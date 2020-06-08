import sys, time
from numpy import linspace
from . import DotDict


def ProgressBar(iterObj):
    def SecToStr(sec):
        m, s = divmod(sec, 60)
        h, m = divmod(m, 60)
        return u'%d:%02d:%02d' % (h, m, s)

    L = len(iterObj)
    steps = {int(x): y for x, y in zip(linspace(0, L, min(100, L), endpoint=False),
                                       linspace(0, 100, min(100, L), endpoint=False))}
    qSteps = ['', u'\u258E', u'\u258C', u'\u258A']  # quarter and half block chars
    startT = time.time()
    timeStr = '   [0:00:00, -:--:--]'
    activity = [' -', ' \\', ' |', ' /']
    for nn, item in enumerate(iterObj):
        if nn in steps:
            done = u'\u2588' * int(steps[nn] / 4.0) + qSteps[int(steps[nn] % 4)]
            todo = ' ' * (25 - len(done))
            barStr = u'%4d%% |%s%s|' % (steps[nn], done, todo)
        if nn > 0:
            endT = time.time()
            timeStr = ' [%s, %s]' % (SecToStr(endT - startT),
                                     SecToStr((endT - startT) * (L / float(nn) - 1)))
        # sys.stdout.write('\r' + barStr + activity[nn % 4] + timeStr);
        # sys.stdout.flush()
        yield item
    barStr = u'%4d%% |%s|' % (100, u'\u2588' * 25)
    timeStr = '   [%s, 0:00:00]\n' % (SecToStr(time.time() - startT))
    # sys.stdout.write('\r' + barStr + timeStr);
    # sys.stdout.flush()


def SecToStr(sec):
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    return u'%d:%02d:%02d' % (h, m, s)


def create(total):
    obj= DotDict.DotDict({
        "total": total,
        "current": 0,
        "start_time": time.time()
    })

    update(obj, 0)

    return obj

def update(progress_bar_obj, current_step=None):
    current = current_step
    if current is None:
        current = progress_bar_obj.current + 1

    currentPorcentage = current*100/progress_bar_obj.total

    L = progress_bar_obj.total
    PARTIAL_STEPS = ['', u'\u258E', u'\u258C', u'\u258A']  # quarter and half block chars
    startT = progress_bar_obj.start_time
    timeStr = '   [0:00:00, -:--:--]'
    activity = [' -', ' \\', ' |', ' /']

    done = u'\u2588' * int(currentPorcentage / 4.0) + PARTIAL_STEPS[int((currentPorcentage) % 4)]
    todo = ' ' * (25 - len(done))
    barStr = u'%4d%% |%s%s|' % (currentPorcentage, done, todo)
    if progress_bar_obj.current > 0:
        endT = time.time()
        timeStr = ' [%s, %s]' % (SecToStr(endT - startT),
                                 SecToStr((endT - startT) * (L / float(currentPorcentage) - 1)))
    # sys.stdout.write('\r' + barStr + activity[int(currentPorcentage % 4)] + timeStr)
    # sys.stdout.flush()

    progress_bar_obj.current = current

def done(progress_bar_obj):
    barStr = u'%4d%% |%s|' % (100, u'\u2588' * 25)
    timeStr = '   [%s, 0:00:00]\n' % (SecToStr(time.time() - progress_bar_obj.start_time))
    # sys.stdout.write('\r' + barStr + timeStr);
