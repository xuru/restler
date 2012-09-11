
def update_method(cls, name, method):
    def method_name(base, count):
        return "_%s_%s" % (name, count)
    if hasattr(cls, name):
        setattr(cls, name, method)
    else:
        count = 0
        for i in range(1, 10):
            count = i
            m_name = method_name(name, i)
            if hasattr(cls, m_name): continue
        for i in range(count, 0, -1):
            m_name = method_name(name, i)
            if i != 1:
                setattr(cls, m_name, method_name(name, i-1) )
            else:
                setattr(cls, m_name, name)


def update_m(cls, name, method):
    if hasattr(cls, name):
        if getattr(cls, name).__func__.func_code.co_argcount == 1:
            result = getattr(cls, name)()

