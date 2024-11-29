class ClubeDosTampinhaError(Exception):
    pass


class UserDoesNotExist(ClubeDosTampinhaError):
    pass


class UserAlreadyExists(ClubeDosTampinhaError):
    pass


class UserRoleDoesNotExist(ClubeDosTampinhaError):
    pass
