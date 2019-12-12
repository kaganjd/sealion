# class for GUI message handling
# singleton behavior described https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html
class MessageSingleton:
    class __MessageSingleton:
        def __init__(self, arg):
            self.val = arg
        def __str__(self):
            return repr(self) + self.val
    instance = None
    def __init__(self, arg):
        if not MessageSingleton.instance:
            MessageSingleton.instance = MessageSingleton.__MessageSingleton(arg)
        else:
            MessageSingleton.instance.val = arg
    def __getattr__(self, name):
        return getattr(self.instance, name)
