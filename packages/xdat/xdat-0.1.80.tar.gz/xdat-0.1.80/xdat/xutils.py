from . import xpd, xnp, xplt


def x_monkey_patch(aggressive=False):
    xpd.monkey_patch(aggressive=aggressive)
    xnp.monkey_patch()
    xplt.monkey_patch()


def split_X_y(df, target):
    df = df.copy()
    y = df[target]
    del df[target]
    return df, y
