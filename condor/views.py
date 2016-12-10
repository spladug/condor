import logging

from pyramid.view import view_config, view_defaults
from pyramid import httpexceptions as exc
from sqlalchemy.orm.exc import NoResultFound

from .models import Poll

logger = logging.getLogger(__name__)


@view_config(route_name="home", renderer="condor:templates/home.jinja2")
def home(context, request):
    return {}


@view_defaults(route_name="polls")
class PollsView(object):
    def __init__(self, request):
        self.request = request

    @view_config(request_method="POST")
    def create_poll(self):
        poll = Poll(
            id=None,
            title=self.request.POST["title"],
            state="open",
            creator_id=self.request.user.id,
            description=self.request.POST["description"],
        )
        self.request.db.add(poll)
        self.request.db.commit()
        return exc.HTTPSeeOther(self.request.route_url("poll", id=poll.id))


@view_defaults(route_name="poll")
class PollView(object):
    def __init__(self, request):
        self.request = request

        poll_id = int(self.request.matchdict["id"])
        try:
            self.poll = request.db.query(Poll).filter_by(id=poll_id).one()
        except NoResultFound:
            raise exc.HTTPNotFound()

    @view_config(request_method="GET", renderer="condor:templates/poll.jinja2")
    def get_poll(self):
        return {
            "poll": self.poll,
        }

    @view_config(request_method="PUT")
    def update_poll(self):
        pass
