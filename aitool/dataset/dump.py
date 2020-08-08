import os
import numpy as np
import lxml.etree as ET

import aitool


class XMLDumperBase():
    """save objects to specific file format
    """
    def __init__(self,
                output_dir,
                classes=None):
        self.output_dir = output_dir
        aitool.mkdir_or_exist(self.output_dir)
        
        self.classes = classes

    def __call__(self, objects, image_fn):
        basename = aitool.get_basename(image_fn)
        root = ET.Element("annotations")
        ET.SubElement(root, "folder").text = 'VOC'
        ET.SubElement(root, "filename").text = image_fn
        
        for data in objects:
            obj = ET.SubElement(root, "object")
            if self.classes is not None:
                ET.SubElement(obj, "name").text = self.classes[data['category_id'] - 1]
            else:
                ET.SubElement(obj, "name").text = str(data['category_id'])
            ET.SubElement(obj, "type").text = "bndbox"

            bndbox = ET.SubElement(obj, "bndbox")
            bbox = data['bbox']
            xmin, ymin, xmax, ymax = aitool.xywh2xyxy(bbox)
            ET.SubElement(bndbox, "xmin").text = str(xmin)
            ET.SubElement(bndbox, "ymin").text = str(ymin)
            ET.SubElement(bndbox, "xmax").text = str(xmax)
            ET.SubElement(bndbox, "ymax").text = str(ymax)
            
        tree = ET.ElementTree(root)
        tree.write(f"{self.output_dir}/{basename}.xml", pretty_print=True, xml_declaration=True, encoding='utf-8')


class XMLDumperPlane(XMLDumperBase):
    """save objects to specific file format (plane competition, http://en.sw.chreos.org/)
    """
    def __call__(self, objects, image_fn):
        basename = aitool.get_basename(image_fn)
        root = ET.Element("annotations")
        source = ET.SubElement(root, "source")
        ET.SubElement(source, "filename").text = basename + '.tif'
        ET.SubElement(source, "origin").text = 'GF2/GF3'

        research = ET.SubElement(root, "research")
        ET.SubElement(research, "version").text = "4.0"
        ET.SubElement(research, "provider").text = "Wuhan University"
        ET.SubElement(research, "author").text = "CAPTAIN-VIPG-Plane"
        ET.SubElement(research, "pluginname").text = "Airplane Detection and Recognition in Optical Images"
        ET.SubElement(research, "pluginclass").text = "Detection"
        ET.SubElement(research, "time").text = "2020-07-2020-11"

        objects_handle = ET.SubElement(root, "objects")
        
        for data in objects:
            obj = ET.SubElement(objects_handle, "object")
            ET.SubElement(obj, "coordinate").text = "pixel"
            ET.SubElement(obj, "type").text = "rectangle"
            ET.SubElement(obj, "description").text = "None"

            possibleresult = ET.SubElement(obj, "possibleresult")
            if self.classes is not None:
                ET.SubElement(possibleresult, "name").text = self.classes[data['category_id'] - 1]
            else:
                ET.SubElement(possibleresult, "name").text = str(data['category_id'])
            ET.SubElement(possibleresult, "probability").text = str(data['score'])

            points = ET.SubElement(obj, "points")
            pointobb = data['pointobb']

            for idx in range(5):
                if idx == 4:
                    idx = 0
                ET.SubElement(points, "point").text = f"{pointobb[2 * idx]},{pointobb[2 * idx + 1]}"
            
        tree = ET.ElementTree(root)
        tree.write(f"{self.output_dir}/{basename}.xml", pretty_print=True, xml_declaration=True, encoding='utf-8')