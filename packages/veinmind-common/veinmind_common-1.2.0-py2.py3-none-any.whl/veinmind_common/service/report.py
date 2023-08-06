import enum
import time as timep
import jsonpickle
import json
import os, stat, pwd, grp
from veinmind import service, log, docker, containerd, image, container, tarball, remote, iac

_namespace = "github.com/chaitin/veinmind-tools/veinmind-common/go/service/report"

# Normalize timezone and format into RFC3339 format.
_timezone = timep.strftime('%z')
assert len(_timezone) == 5
if _timezone == "+0000" or _timezone == "-0000":
    _timezone = "Z"
else:
    _timezone = _timezone[0:3] + ':' + _timezone[3:5]
_format = "%Y-%m-%dT%H:%M:%S" + _timezone


@enum.unique
class Level(enum.Enum):
    Low = 0
    Medium = 1
    High = 2
    Critical = 3


@enum.unique
class DetectType(enum.Enum):
    Image = 0
    Container = 1


@enum.unique
class EventType(enum.Enum):
    Risk = 0
    Invasion = 1


@enum.unique
class AlertType(enum.Enum):
    Vulnerability = 0
    MaliciousFile = 1
    Backdoor = 2
    Sensitive = 3
    AbnormalHistory = 4
    Weakpass = 5


class FileDetail():
    path = ""
    perm = 0
    size = 0
    gname = ""
    gid = 0
    uname = ""
    uid = 0
    ctim = 0
    mtim = 0
    atim = 0

    def __init__(self, path, perm, size, gid, uid, ctim, mtim, atim, gname, uname) -> None:
        self.path = path
        self.perm = perm
        self.size = size
        self.gname = gname
        self.gid = gid
        self.uname = uname
        self.uid = uid
        self.ctim = ctim
        self.mtim = mtim
        self.atim = atim

    @classmethod
    def from_stat(cls, path, file_stat):
        return cls(path=path, perm=stat.S_IMODE(file_stat.st_mode), size=file_stat.st_size, gid=file_stat.st_gid,
                   uid=file_stat.st_uid, ctim=int(file_stat.st_ctime), mtim=int(file_stat.st_mtime),
                   atim=int(file_stat.st_atime), uname=pwd.getpwuid(file_stat.st_uid).pw_name,
                   gname=grp.getgrgid(file_stat.st_gid).gr_name)


class HistoryDetail():
    instruction = ""
    content = ""
    description = ""

    def __init__(self, instruction, content, description):
        self.instruction = instruction
        self.content = content
        self.description = description


class SensitiveFileDetail(FileDetail):
    rule_id = 0
    rule_name = ""
    rule_description = ""

    def __init__(self, rule_id, rule_name, rule_description, file_detail):
        self.rule_id = rule_id
        self.rule_name = rule_name
        self.rule_description = rule_description
        super().__init__(file_detail.path, file_detail.perm, file_detail.size, file_detail.gid, file_detail.uid,
                         file_detail.ctim, file_detail.mtim, file_detail.atim, file_detail.uname, file_detail.gname)


class SensitiveEnvDetail():
    key = ""
    value = ""
    rule_id = 0
    rule_name = ""
    rule_description = ""

    def __init__(self, key, value, rule_id, rule_name, rule_description):
        self.key = key
        self.value = value
        self.rule_id = rule_id
        self.rule_name = rule_name
        self.rule_description = rule_description


class SensitiveDockerHistoryDetail():
    value = ""
    rule_id = 0
    rule_name = ""
    rule_description = ""

    def __init__(self, value, rule_id, rule_name, rule_description):
        self.value = value
        self.rule_id = rule_id
        self.rule_name = rule_name
        self.rule_description = rule_description


class BackdoorDetail(FileDetail):
    description = ""

    def __init__(self, description, file_detail):
        self.description = description
        super().__init__(file_detail.path, file_detail.perm, file_detail.size, file_detail.gid, file_detail.uid,
                         file_detail.ctim, file_detail.mtim, file_detail.atim, file_detail.uname, file_detail.gname)


class AlertDetail:
    backdoor_detail = None
    sensitive_file_detail = None
    sensitive_env_detail = None
    sensitive_docker_history_detail = None
    history_detail = None

    def __init__(self, backdoor_detail=None, sensitve_file_detail=None,
                 sensitive_env_detail=None, sensitive_docker_history_detail=None, history_detail=None):
        self.backdoor_detail = backdoor_detail
        self.sensitive_file_detail = sensitve_file_detail
        self.sensitive_env_detail = sensitive_env_detail
        self.sensitive_docker_history_detail = sensitive_docker_history_detail
        self.history_detail = history_detail

    @classmethod
    def backdoor(cls, backdoor_detail):
        return cls(backdoor_detail=backdoor_detail)

    @classmethod
    def sensitive_file(cls, sensitve_file_detail):
        return cls(sensitve_file_detail=sensitve_file_detail)

    @classmethod
    def sensitive_env(cls, sensitive_env_detail):
        return cls(sensitive_env_detail=sensitive_env_detail)

    @classmethod
    def sensitive_docker_history(cls, sensitive_docker_history_detail):
        return cls(sensitive_docker_history_detail=sensitive_docker_history_detail)

    @classmethod
    def history(cls, history_detail):
        return cls(history_detail=history_detail)


class ReportEvent():
    id = ""
    time = ""
    level = 0
    detect_type = 0
    event_type = 0
    alert_type = 0
    alert_details = []

    def __init__(self, id, level, detect_type, event_type, alert_type,
                 alert_details, native_object, t=timep.strftime(_format)):
        self.id = id
        self.object = NativeObject(native_object)
        self.time = t
        self.level = level
        self.detect_type = detect_type
        self.event_type = event_type
        self.alert_type = alert_type
        self.alert_details = alert_details


class NativeObject():
    def __init__(self, object):
        self.raw = object

        # runtime type
        if isinstance(object, docker.Image) or isinstance(object, docker.Container):
            self.runtime_type = "docker"
        elif isinstance(object, containerd.Image) or isinstance(object, containerd.Container):
            self.runtime_type = "containerd"
        elif isinstance(object, remote.Image):
            self.runtime_type = "remote"
        elif isinstance(object, tarball.Image):
            self.runtime_type = "tarball"

        # object type
        if isinstance(object, image.Image):
            self.type = "image"
            self.id = object.id()
        elif isinstance(object, container.Container):
            self.type = "container"
            self.id = object.id()
        elif isinstance(object, iac.IAC):
            self.type = "iac"
            self.id = object.path

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['raw']
        return state

@service.service(_namespace, "report")
def _report(evt):
    pass


def report(evt, *args, **kwargs):
    if service.is_hosted():
        try:
            evt_dict = json.loads(jsonpickle.encode(evt, unpicklable=False))
            _report(evt_dict)
        except RuntimeError as e:
            log.error(e)
    else:
        log.warn(jsonpickle.encode(evt, indent=4, unpicklable=False))


class Entry:
    def __init__(self, **kwargs):
        self.fields = kwargs.copy()

    def report(self, evt):
        report(evt)
