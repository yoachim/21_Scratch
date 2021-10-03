import numpy as np
import matplotlib.pylab as plt

# Starting with example at
# https://matplotlib.org/examples/api/radar_chart.html

from matplotlib.path import Path
from matplotlib.spines import Spine
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection


def radar_factory(num_vars, frame='circle'):
    """Create a radar chart with `num_vars` axes.

    This function creates a RadarAxes projection and registers it.

    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    frame : {'circle' | 'polygon'}
        Shape of frame surrounding axes.

    """
    # calculate evenly-spaced axis angles
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)
    # rotate theta such that the first axis is at the top
    theta += np.pi/2
    # FFS, need to make sure we don't go over 360
    theta = theta % (2.*np.pi)

    def draw_poly_patch(self):
        verts = unit_poly_verts(theta)
        return plt.Polygon(verts, closed=True, edgecolor='k')

    def draw_circle_patch(self):
        # unit circle centered on (0.5, 0.5)
        return plt.Circle((0.5, 0.5), 0.5)

    patch_dict = {'polygon': draw_poly_patch, 'circle': draw_circle_patch}
    if frame not in patch_dict:
        raise ValueError('unknown value for `frame`: %s' % frame)

    class RadarAxes(PolarAxes):

        name = 'radar'
        # use 1 line segment to connect specified points
        RESOLUTION = 1
        # define draw_frame method
        draw_patch = patch_dict[frame]

        def fill(self, *args, **kwargs):
            """Override fill so that line is closed by default"""
            closed = kwargs.pop('closed', True)
            return super(RadarAxes, self).fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super(RadarAxes, self).plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.concatenate((x, [x[0]]))
                y = np.concatenate((y, [y[0]]))
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            return self.draw_patch()

        def _gen_axes_spines(self):
            if frame == 'circle':
                return PolarAxes._gen_axes_spines(self)
            # The following is a hack to get the spines (i.e. the axes frame)
            # to draw correctly for a polygon frame.

            # spine_type must be 'left', 'right', 'top', 'bottom', or `circle`.
            spine_type = 'circle'
            verts = unit_poly_verts(theta)
            # close off polygon by repeating first vertex
            verts.append(verts[0])
            path = Path(verts)

            spine = Spine(self, spine_type, path)
            spine.set_transform(self.transAxes)
            return {'polar': spine}

    register_projection(RadarAxes)
    return theta


def unit_poly_verts(theta):
    """Return vertices of polygon for subplot axes.

    This polygon is circumscribed by a unit circle centered at (0.5, 0.5)
    """
    x0, y0, r = [0.5] * 3
    verts = [(r*np.cos(t) + x0, r*np.sin(t) + y0) for t in theta]
    return verts


def radar(df, legend_col='runName', rgrids=[0.7, 1.0, 1.3, 1.6],
          alpha=0.1, legend=True, figsize=(8.5, 5), fill=False,
          bbox_to_anchor=(1.6, 0.5)):
    """
    make a radar plot!
    """
    theta = radar_factory(np.size(df.columns) - 1, frame='polygon')
    fig, axes = plt.subplots(figsize=figsize, subplot_kw=dict(projection='radar'))
    axes.set_rgrids(rgrids)

    for i, lname in enumerate(df[legend_col]):
        data = df.loc[:, df.columns != legend_col].iloc[i]
        if np.size(data) > 0:
            axes.plot(theta, data.values, 'o-', label=df[legend_col].iloc[i])
            if fill:
                axes.fill(theta, data.values, alpha=alpha)

    varlables = [col for col in df.columns if col != legend_col]

    axes.set_varlabels(varlables)
    if legend:
        axes.legend(bbox_to_anchor=bbox_to_anchor, borderaxespad=0, loc='lower right')
    axes.set_ylim([np.min(rgrids), np.max(rgrids)])

    return fig, axes


def radar2(df, legend_col='runName', rgrids=[[0.7, 1.0, 1.3, 1.6], [0.9, 1.0, 1.1]],
           alpha=0.1, legend=True, figsize=(13, 5), fill=False,
           bbox_to_anchor=(1.7, 0.5)):
    """
    make a radar plot!
    """
    theta = radar_factory(np.size(df.columns) - 1, frame='polygon')
    fig, ax = plt.subplots(1, 2, figsize=figsize, subplot_kw=dict(projection='radar'))
    for axes, rgrid in zip(ax, rgrids):
        axes.set_rgrids(rgrid)
        for i, lname in enumerate(df[legend_col]):
            data = df.loc[:, df.columns != legend_col].iloc[i]
            if np.size(data) > 0:
                axes.plot(theta, data.values, 'o-', label=df[legend_col].iloc[i])
                if fill:
                    axes.fill(theta, data.values, alpha=alpha)

        varlables = [col for col in df.columns if col != legend_col]

        axes.set_varlabels(varlables)
        if legend:
            axes.legend(bbox_to_anchor=bbox_to_anchor, borderaxespad=0, loc='lower right')
            legend = False
    # Why didn't this work in the above loop?
    for i, _temp in enumerate(rgrids):
        ax[i].set_rgrids(rgrids[i])
        ax[i].set_rgrids(rgrids[i])
        ax[i].set_ylim([np.min(rgrids[i]), np.max(rgrids[i])])

    return fig, ax


def norm_df(df, runs, cols, norm_run='baseline_nexp1_v1.6',
            invert_cols=None, reverse_cols=None, row_label='runName', mag_cols=[]):
    """
    Normalize values in a dataframe to a given column
    """
    indices = [np.max(np.where(df[row_label] == name)[0]) for name in runs]
    out_df = df[cols].loc[indices].copy()
    if reverse_cols is not None:
        for colname in reverse_cols:
            out_df[colname] = -out_df[colname]
    if invert_cols is not None:
        for colname in invert_cols:
            out_df[colname] = 1./out_df[colname]
    if norm_run is not None:
        indx = np.max(np.where(out_df[row_label] == norm_run)[0])
        for col in out_df.columns:
            # maybe just check that it's not a
            if col != 'runName':
                if (col in mag_cols) | (mag_cols == 'all'):
                    out_df[col] = 1. + (out_df[col] - out_df[col].iloc[indx])
                else:
                    out_df[col] = 1. + (out_df[col] - out_df[col].iloc[indx])/out_df[col].iloc[indx]
    return out_df
