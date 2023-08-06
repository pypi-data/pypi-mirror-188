import jax.numpy as jnp
from fortuna.typing import Array
from typing import List, Callable


class EnbPI:
    def conformal_interval(
            self,
            cross_val_outputs: List[List[Array]],
            targets: List[Array],
            cross_test_outputs: List[List[Array]],
            error: float,
            aggr_fun: Callable[[List[Array]], Array]
    ) -> jnp.ndarray:
        aggr_test_outputs = jnp.concatenate([aggr_fun(outputs) for outputs in cross_test_outputs], 0)
        jnp.quantile(aggr_test_outputs, q=1 - error)


        r = [jnp.abs(y - mu) for y, mu in zip(cross_val_targets, cross_val_outputs)]
        left = jnp.concatenate([mu[None] - ri[:, None] for mu, ri in zip(cross_test_outputs, r)], 0)
        right = jnp.concatenate([mu[None] + ri[:, None] for mu, ri in zip(cross_test_outputs, r)])

        qleft = jnp.quantile(left, q=error, axis=0)
        qright = jnp.quantile(right, q=1 - error, axis=0)
        return jnp.array(list(zip(qleft, qright))).squeeze(2)
