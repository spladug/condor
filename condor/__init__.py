import logging

from baseplate import make_metrics_client, config, Baseplate
from baseplate.context.sqlalchemy import SQLAlchemySessionContextFactory
from baseplate.integration.pyramid import BaseplateConfigurator
from pyramid.authentication import RemoteUserAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory
from sqlalchemy import engine_from_config

from .models import User


logger = logging.getLogger(__name__)


def get_authenticated_user(request):
    return User.by_email(request.db, request.authenticated_userid)


def make_wsgi_app(app_config):
    cfg = config.parse_config(app_config, {
        "session": {
            "secret": config.Base64,
        }
    })

    # configure pyramid
    configurator = Configurator(settings=app_config)
    configurator.include("pyramid_jinja2")

    configurator.set_default_csrf_options(require_csrf=True)
    configurator.set_session_factory(SignedCookieSessionFactory(cfg.session.secret))

    authn_policy = RemoteUserAuthenticationPolicy(environ_key="HTTP_AUTHENTICATED_USER")
    authz_policy = ACLAuthorizationPolicy()
    configurator.set_authentication_policy(authn_policy)
    configurator.set_authorization_policy(authz_policy)
    configurator.add_request_method(get_authenticated_user, "user", reify=True)

    configurator.add_static_view(name="static", path="condor:static/")
    configurator.add_route("home", "/")
    configurator.add_route("polls", "/polls")
    configurator.add_route("poll", "/polls/{id:\d+}")
    configurator.scan("condor.views")

    # configure baseplate
    metrics_client = make_metrics_client(app_config)

    baseplate = Baseplate()
    baseplate.configure_logging()
    baseplate.configure_metrics(metrics_client)

    engine = engine_from_config(app_config, prefix="database.")
    baseplate.add_to_context("db", SQLAlchemySessionContextFactory(engine))

    baseplate_configurator = BaseplateConfigurator(baseplate)
    configurator.include(baseplate_configurator.includeme)

    return configurator.make_wsgi_app()
