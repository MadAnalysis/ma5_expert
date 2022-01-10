#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 11:24:20 2020

@author: jackaraz
"""

import os, copy, json


class SAF:
    def __init__(self, **kwargs):
        self.saf_file = False
        self.saf = {}
        if kwargs.get("saf_file", False) != False:
            if os.path.isfile(kwargs.get("saf_file", "NaN")):
                self.saf_file = kwargs.get("saf_file", "NaN")
            else:
                raise ValueError("Can not find the SAF file!")
        if kwargs.get("load", False) == False and self.saf_file != False:
            self.saf = self.saf_parse()
        elif kwargs.get("load", False) != False:
            self.saf = self.load(kwargs.get("load", False))
        self.saf = self.set_xsec(kwargs.get("xsection", -1))

    def __getattr__(self, name):
        if name in self.saf["SampleGlobalInfo"].keys() + ["xsection"]:
            if name == "xsection":
                name = "xsec"
            return self.saf["SampleGlobalInfo"][name]
        elif name in self.saf.keys():
            return self.saf[name]
        else:
            return False

    def load(self, json_file):
        if os.path.isfile(json_file):
            with open(json_file, "r") as json_file:
                saf = json.load(json_file)
        else:
            return {}
        return saf

    def save(self, **kwargs):
        try:
            output = kwargs.get("output", False)
            if output == False:
                output = self.saf_file.split(".saf")[0] + ".json"
            out = open(output, "w")
            out.write(json.dumps(self.saf, indent=4))
            out.close()
        except:
            return False
        return True

    def saf_parse(self, **kwargs):
        saf_file = kwargs.get("saf_file", False)
        if saf_file == False:
            saf_file = self.saf_file
        with open(saf_file) as f:
            saf = f.readlines()
        parsed = {
            "SampleGlobalInfo": {"xsec": -1, "Nevents": -1, "sumw": -1},
            "FileInfo": [],
            "SampleDetailedInfo": {},
        }
        SampleGlobalInfo = [0, 0]
        FileInfo = [0, 0]
        SampleDetailedInfo = [0, 0]
        for n, (line) in enumerate(saf):
            if "<SampleGlobalInfo>" in line:
                SampleGlobalInfo[0] = n
            elif "</SampleGlobalInfo>" in line:
                SampleGlobalInfo[1] = n
            elif "<FileInfo>" in line:
                FileInfo[0] = n
            elif "</FileInfo>" in line:
                FileInfo[1] = n
            elif "<SampleDetailedInfo>" in line:
                SampleDetailedInfo[0] = n
            elif "</SampleDetailedInfo>" in line:
                SampleDetailedInfo[1] = n
        parsed["SampleGlobalInfo"] = saf[SampleGlobalInfo[0] + 2 : SampleGlobalInfo[1]]
        parsed["FileInfo"] = saf[FileInfo[0] + 1 : FileInfo[1]]
        SampleDetailedInfo = saf[SampleDetailedInfo[0] + 2 : SampleDetailedInfo[1]]

        parsed["SampleGlobalInfo"] = {
            "xsec": float(parsed["SampleGlobalInfo"][0].split()[0]),
            "Nevents": int(parsed["SampleGlobalInfo"][0].split()[2]),
            "sumw": float(parsed["SampleGlobalInfo"][0].split()[3])
            - float(parsed["SampleGlobalInfo"][0].split()[4]),
        }
        parsed["FileInfo"] = [x.split(" ")[0][1:-1] for x in parsed["FileInfo"]]

        for n, (line) in enumerate(SampleDetailedInfo):
            parsed["SampleDetailedInfo"][int(n)] = {
                "xsec": float(line.split()[0]),
                "Nevents": int(line.split()[2]),
                "sumw": float(line.split()[3]) - float(line.split()[4]),
            }
        return parsed

    def set_xsec(self, xsection):
        saf = copy.deepcopy(self.saf)
        if xsection > 0.0 and saf != {}:
            saf["SampleGlobalInfo"]["xsec"] = float(xsection)
        return saf

    def get_detailedXsec(self):
        xsec = 0.0
        nevt = 0.0
        for nfile, info in self.saf["SampleDetailedInfo"].items():
            xsec += info["xsec"] * info["Nevents"]
            nevt += info["Nevents"]
        if nevt > 0.0:
            return round(xsec / nevt, 8)
        else:
            return 0.0

    def get_xsec(self):
        return self.saf["SampleGlobalInfo"]["xsec"]
