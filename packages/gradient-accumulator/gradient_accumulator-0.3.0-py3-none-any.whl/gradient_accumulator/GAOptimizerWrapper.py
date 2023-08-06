import tensorflow as tf
from tensorflow_addons.utils import types
from typeguard import typechecked


# Implementation was derived from:
# https://github.com/fsx950223/addons/blob/67c1e8ea19e82c3f2a5706674dd81f15ab5002a2/tensorflow_addons/optimizers/gradient_accumulator.py
@tf.keras.utils.register_keras_serializable()
class GAOptimizerWrapper(tf.keras.optimizers.Optimizer):
    """Optimizer wrapper for gradient accumulation."""
    @typechecked
    def __init__(
        self,
        optimizer: types.Optimizer,
        accum_steps: types.TensorLike = 4,
        reduction: str = "MEAN",
        name: str = "GAOptimizerWrapper",
        **kwargs,
    ):
        r"""Construct a new GAOptimizerWrapper optimizer.

        Args:
            optimizer: str or `tf.keras.optimizers.Optimizer` that will be
                used to compute and apply gradients.
            accum_steps: int > 0. Update gradient in every accumulation steps.
            reduction: str. Which gradient reduction method to use. Defaults to 'SUM'.
            name: Optional name for the operations created when applying
                gradients. Defaults to "GAOptimizerWrapper".
            **kwargs: keyword arguments. Allowed to be {`clipnorm`,
                `clipvalue`, `lr`, `decay`}. `clipnorm` is clip gradients by
                norm; `clipvalue` is clip gradients by value, `decay` is
                included for backward compatibility to allow time inverse
                decay of learning rate. `lr` is included for backward
                compatibility, recommended to use `learning_rate` instead.
        """
        self.optimizer = optimizer
        self._optimizer = tf.keras.optimizers.get(optimizer)
        self.reduction = reduction
        self._gradients = []
        self._accum_steps = accum_steps
        super().__init__(name, **kwargs)

    def _create_slots(self, var_list):
        self._optimizer._create_slots(var_list=var_list)
        for var in var_list:
            self.add_slot(var, "ga")

        self._gradients = [self.get_slot(var, "ga") for var in var_list]

    @property
    def gradients(self):
        """The accumulated gradients on the current replica."""
        if not self._gradients:
            raise ValueError(
                "The accumulator should be called first to initialize the gradients"
            )
        return list(
            gradient.read_value() if gradient is not None else gradient
            for gradient in self._gradients
        )

    def apply_gradients(self, grads_and_vars, name=None, **kwargs):
        self._optimizer._iterations = self.iterations
        return super().apply_gradients(grads_and_vars, name, **kwargs)

    @tf.function
    def _resource_apply_dense(self, grad, var, apply_state=None):
        accum_gradient = self.get_slot(var, "ga")

        if accum_gradient is not None and grad is not None:
            if self.reduction == "MEAN":
                grad /= tf.cast(self._accum_steps, grad.dtype)

            accum_gradient.assign_add(
                grad, use_locking=self._use_locking, read_value=False
            )

        def _apply():
            if "apply_state" in self._optimizer._dense_apply_args:
                train_op = self._optimizer._resource_apply_dense(
                    accum_gradient.read_value(), var, apply_state=apply_state
                )
            else:
                train_op = self._optimizer._resource_apply_dense(
                    accum_gradient.read_value(), var
                )
            reset_op = accum_gradient.assign(
                        tf.zeros_like(accum_gradient),
                        use_locking=self._use_locking,
                        read_value=False,
                    )
            return tf.group(train_op, reset_op)

        apply_op = tf.cond(
            (self.iterations + 1) % self._accum_steps == 0, _apply, lambda: tf.no_op()
        )
        return apply_op

    @tf.function
    def _resource_apply_sparse(self, grad: types.TensorLike, var, indices, apply_state):
        accum_gradient = self.get_slot(var, "ga")
        if accum_gradient is not None and grad is not None:
            self._resource_scatter_add(accum_gradient, indices, grad)

        def _apply():
            if "apply_state" in self._optimizer._sparse_apply_args:
                train_op = self._optimizer._resource_apply_sparse(
                    accum_gradient.sparse_read(indices),
                    var,
                    indices,
                    apply_state=apply_state,
                )
            else:
                train_op = self._optimizer._resource_apply_sparse(
                    accum_gradient.sparse_read(indices), var, indices
                )
            reset_op = accum_gradient.assign(
                        tf.zeros_like(accum_gradient),
                        use_locking=self._use_locking,
                        read_value=False,
                    )
            return tf.group(train_op, reset_op)

        apply_op = tf.cond(
            (self.iterations + 1) % self._accum_steps == 0, _apply, lambda: tf.no_op()  # tf.no_op: Does nothing - placeholder
        )
        return apply_op

    def reset(self):
        """Resets the accumulated gradients on the current replica."""
        assign_ops = []
        if not self._gradients:
            return assign_ops

        for gradient in self._gradients:
            if gradient is not None:
                assign_ops.append(
                    gradient.assign(
                        tf.zeros_like(gradient),
                        use_locking=self._use_locking,
                        read_value=False,
                    )
                )

        return tf.group(assign_ops)

    @property
    def lr(self):
        return self._optimizer._get_hyper("learning_rate")

    @lr.setter
    def lr(self, lr):
        self._optimizer._set_hyper("learning_rate", lr)

    @property
    def learning_rate(self):
        return self._optimizer._get_hyper("learning_rate")

    @learning_rate.setter
    def learning_rate(self, learning_rate):
        self._optimizer._set_hyper("learning_rate", learning_rate)

    def get_config(self):
        config = super(GAOptimizerWrapper, self).get_config()
        config.update({
            "optimizer": self.optimizer,
            "accum_steps": self._accum_steps,
            "reduction": self.reduction})
        return config
