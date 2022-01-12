
from functools import partial

import jax
from jax.scipy.optimize import minimize

from . import MuseProblem


class JaxMuseProblem(MuseProblem):

    def logLike(self, x, z, θ):
        raise NotImplementedError()

    def logPrior(self, θ):
        raise NotImplementedError()

    def gradθ_logLike(self, x, z, θ):
        return jax.grad(lambda θ: self.logLike(x, z, θ))(θ)

    def logLike_and_gradz_logLike(self, x, z, θ):
        logLike = self.logLike(x, z, θ)
        gradz_logLike = jax.grad(lambda z: self.logLike(x, z, θ))(z)
        return (logLike, gradz_logLike)

    def zMAP_at_θ(self, x, z0, θ, gradz_logLike_atol=None):
        soln = minimize(lambda z: -self.logLike(x, z, θ), z0, method="BFGS", tol=gradz_logLike_atol)
        return (soln.x, soln)

    def grad_hess_θ_logPrior(self, θ):
        g = jax.grad(self.logPrior)(θ)
        H = jax.hessian(self.logPrior)(θ)
        return (g,H)


class JittedJaxMuseProblem(JaxMuseProblem):

    @partial(jax.jit, static_argnums=(0,))
    def gradθ_logLike(self, x, z, θ):
        return super().gradθ_logLike(x, z, θ)

    @partial(jax.jit, static_argnums=(0,))
    def logLike_and_gradz_logLike(self, x, z, θ):
        return super().logLike_and_gradz_logLike(x, z, θ)

    @partial(jax.jit, static_argnums=(0,))
    def zMAP_at_θ(self, x, z0, θ, gradz_logLike_atol=None):
        return super().zMAP_at_θ(x, z0, θ, gradz_logLike_atol)

    @partial(jax.jit, static_argnums=(0,))
    def grad_hess_θ_logPrior(self, θ):
        return super().grad_hess_θ_logPrior(θ)
