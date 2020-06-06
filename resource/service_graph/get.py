from document.exec_env import ExecEnvDocument
from http import HTTPStatus


def get_default(policy, results):
    default = policy.get('default', None)
    if default is not None and default not in ['forwardAll']:
        results.append(dict(status='error', error=True, description='Default action unknown.',
                            data=policy, http_status_code=HTTPStatus.CONFLICT))
    return default


def get_exec_env(policy, direction, results):
    exec_env_id = policy.get(direction, None)
    if exec_env_id is None:
        results.append(dict(status='error', error=True, description=f'Missing [{direction}] service in the policy.',
                            data=policy, http_status_code=HTTPStatus.CONFLICT))
        return None
    exec_env = ExecEnvDocument.get(id=exec_env_id, ignore=404)
    if exec_env is None:
        results.append(dict(status='error', error=True, description=f'[{direction}] service not found.',
                            data=policy, http_status_code=HTTPStatus.CONFLICT))
    return exec_env


def get_action(policy, results):
    action = policy.get('action', None)
    if action is None:
        results.append(dict(status='error', error=True, description='Missing [action] in the policy.',
                            data=policy, http_status_code=HTTPStatus.CONFLICT))
    elif action not in ['forward', 'deny']:
        results.append(dict(status='error', error=True, description=f'Action policy unknown.',
                            data=policy, http_status_code=HTTPStatus.CONFLICT))
    return action
