#!/usr/bin/env python

"""
Visualization of detected object(s).

TODO:
 - preselect (highlight)
 - display additional information on highlight
 - diameter based on boundingbox size?

"""

from PyQt4 import QtGui, QtCore
from item import Item
from desc_item import DescItem

translate = QtCore.QCoreApplication.translate


class ObjectItem(Item):

    def __init__(self, scene, rpm, object_id, object_type, x, y, yaw,  sel_cb=None, outline_diameter=0.1, selected=False):

        self.object_id = object_id
        self.outline_diameter = outline_diameter
        self.selected = selected
        self.sel_cb = sel_cb
        self.object_type = object_type
        self.inflate = 2.0
        self.hover_ratio = 1.3

        self.desc = None

        super(ObjectItem, self).__init__(scene, rpm, x, y)

        self.desc = DescItem(scene, rpm, 0,  0, self)
        self.desc.setFlag(QtGui.QGraphicsItem.ItemIgnoresTransformations)

        self.update_text()

        self.setRotation(yaw)

        if selected:
            self.set_selected()

    def set_pos(self, x, y, parent_coords=False,  yaw=0.0):

        super(ObjectItem, self).set_pos(x, y,  parent_coords,  yaw)

        if self.desc is not None:
            print self.sceneBoundingRect().height()/2
            self.desc.setPos(-self.boundingRect().width()/2, self.sceneBoundingRect().height()/2 + self.m2pix(0.01))

    def update_text(self):

        desc = []
        desc.append(translate("ObjectItem", "ID: ") + self.object_id)

        if self.hover:

            desc.append(translate("ObjectItem", "TYPE: ") + self.object_type.name)
            desc.append(self.get_pos_str())

        self.desc.set_content(desc)

    def hover_changed(self):

        self.update_text()
        self.update()

    def boundingRect(self):

        lx = self.hover_ratio*self.inflate*self.m2pix(self.object_type.bbox.dimensions[0])
        ly = self.hover_ratio*self.inflate*self.m2pix(self.object_type.bbox.dimensions[1])
        p = 1.0
        return QtCore.QRectF(-lx / 2 - p, -ly / 2 - p, lx + 2 * p, ly + 2 * p)

    def shape(self):

        lx = self.hover_ratio*self.inflate*self.m2pix(self.object_type.bbox.dimensions[0])
        ly = self.hover_ratio*self.inflate*self.m2pix(self.object_type.bbox.dimensions[1])
        p = 1.0
        path = QtGui.QPainterPath()
        path.addRect(-lx / 2 - p, -ly / 2 - p, lx + 2 * p, ly + 2 * p)
        return path

    def paint(self, painter, option, widget):

        painter.setClipRect(option.exposedRect)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        lx = self.inflate*self.m2pix(self.object_type.bbox.dimensions[0])
        ly = self.inflate*self.m2pix(self.object_type.bbox.dimensions[1])

        rr = 10

        if self.selected:

            painter.setBrush(QtCore.Qt.green)
            painter.setPen(QtCore.Qt.green)

            painter.drawRoundedRect(-lx/2*self.hover_ratio,  -ly/2*self.hover_ratio,  lx*self.hover_ratio,  ly*self.hover_ratio,  rr, rr,  QtCore.Qt.RelativeSize)

        elif self.hover:

            painter.setBrush(QtCore.Qt.gray)
            painter.setPen(QtCore.Qt.gray)

            painter.drawRoundedRect(-lx/2*self.hover_ratio,  -ly/2*self.hover_ratio,  lx*self.hover_ratio,  ly*self.hover_ratio,  rr, rr,  QtCore.Qt.RelativeSize)

        painter.setBrush(QtCore.Qt.white)
        painter.setPen(QtCore.Qt.white)

        painter.drawRoundedRect(-lx/2,  -ly/2,  lx,  ly,  rr, rr,  QtCore.Qt.RelativeSize)

        fr = 1.0 - (self.hover_ratio - 1.0) # fill ratio

        painter.setBrush(QtCore.Qt.black)
        painter.setPen(QtCore.Qt.black)
        painter.drawRoundedRect(-lx/2*fr,  -ly/2*fr,  lx*fr,  ly*fr,  rr, rr,  QtCore.Qt.RelativeSize)

    def cursor_press(self):  # TODO cursor_click??

        if self.sel_cb is not None:
            # callback should handle object selection
            self.sel_cb(self.object_id, self.selected)

        else:
            # no callback - object will handle its selection
            if not self.selected:
                self.set_selected()
            else:
                self.set_selected(False)

    def set_selected(self, selected=True):

        if selected:

            self.selected = True
            # rospy.logdebug('Object ID ' + self.object_id + ' selected')

        else:

            self.selected = False
            # rospy.logdebug('Object ID ' + self.object_id + ' unselected')

        self.update()
