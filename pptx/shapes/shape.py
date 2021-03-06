# encoding: utf-8

"""
Base shape-related objects such as BaseShape.
"""

from __future__ import absolute_import, print_function

from warnings import warn


class BaseShape(object):
    """
    Base class for shape objects, including |Shape|, |Picture|, and
    |GraphicFrame|.
    """
    def __init__(self, shape_elm, parent):
        super(BaseShape, self).__init__()
        self._element = shape_elm
        self._parent = parent

    @property
    def element(self):
        """
        Reference to the lxml element for this shape, e.g. a CT_Shape
        instance.
        """
        return self._element

    @property
    def has_chart(self):
        """
        |True| if this shape is a graphic frame containing a chart object.
        |False| otherwise. When |True|, the chart object can be accessed
        using the ``.chart`` property.
        """
        # This implementation is unconditionally False, the True version is
        # on GraphicFrame subclass.
        return False

    @property
    def has_table(self):
        """
        |True| if this shape is a graphic frame containing a table object.
        |False| otherwise. When |True|, the table object can be accessed
        using the ``.table`` property.
        """
        # This implementation is unconditionally False, the True version is
        # on GraphicFrame subclass.
        return False

    @property
    def has_text_frame(self):
        """
        |True| if this shape can contain text.
        """
        # overridden on Shape to return True. Only <p:sp> has text frame
        return False

    @property
    def has_textframe(self):
        """
        Deprecated. Use :attr:`has_text_frame` property instead.
        """
        msg = (
            'Shape.has_textframe property is deprecated. Use .has_text_frame'
            ' instead.'
        )
        warn(msg, UserWarning, stacklevel=2)
        return self.has_text_frame

    @property
    def height(self):
        """
        Read/write. Integer distance between top and bottom extents of shape
        in EMUs
        """
        return self._element.cy

    @height.setter
    def height(self, value):
        self._element.cy = value

    @property
    def id(self):
        """
        Read-only positive integer identifying this shape. The id of a shape
        is unique among all shapes on a slide.
        """
        return self._element.shape_id

    @property
    def is_placeholder(self):
        """
        True if this shape is a placeholder. A shape is a placeholder if it
        has a <p:ph> element.
        """
        return self._element.has_ph_elm

    @property
    def left(self):
        """
        Read/write. Integer distance of the left edge of this shape from the
        left edge of the slide, in English Metric Units (EMU)
        """
        return self._element.x

    @left.setter
    def left(self, value):
        self._element.x = value

    @property
    def name(self):
        """
        Name of this shape, e.g. 'Picture 7'
        """
        return self._element.shape_name

    @name.setter
    def name(self, value):
        self._element._nvXxPr.cNvPr.name = value

    @property
    def part(self):
        """
        The package part containing this object, a _BaseSlide subclass in
        this case.
        """
        return self._parent.part

    @property
    def rotation(self):
        """
        Read/write float. Degrees of clockwise rotation. Negative values can
        be assigned to indicate counter-clockwise rotation, e.g. assigning
        -45.0 will change setting to 315.0.
        """
        return self._element.rot

    @rotation.setter
    def rotation(self, value):
        self._element.rot = value

    @property
    def shape_type(self):
        """
        Unique integer identifying the type of this shape, like
        ``MSO_SHAPE_TYPE.CHART``. Must be implemented by subclasses.
        """
        # # This one returns |None| unconditionally to account for shapes
        # # that haven't been implemented yet, like group shape and chart.
        # # Once those are done this should raise |NotImplementedError|.
        # msg = 'shape_type property must be implemented by subclasses'
        # raise NotImplementedError(msg)
        return None

    @property
    def top(self):
        """
        Read/write. Integer distance of the top edge of this shape from the
        top edge of the slide, in English Metric Units (EMU)
        """
        return self._element.y

    @top.setter
    def top(self, value):
        self._element.y = value

    @property
    def width(self):
        """
        Read/write. Integer distance between left and right extents of shape
        in EMUs
        """
        return self._element.cx

    @width.setter
    def width(self, value):
        self._element.cx = value
