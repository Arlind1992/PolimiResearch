#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 11:37:27 2019

@author: arlind
"""
import pandas as pd

def molecules_not_integrated(orig,after_join):
    moltest1=pd.DataFrame(orig['GMD AS ID'].unique())
    moltest2=pd.DataFrame(after_join['GMD AS ID'].unique())
    moltest1.columns=['Molecule']
    moltest1['Molecule1']=moltest1['Molecule']
    moltest2.columns=['Molecule']
    moltest2['Molecule1']=moltest2['Molecule']
    diff=moltest1.merge(moltest2,how='left',suffixes=('_internal','_external'),on=('Molecule'))
    diff=diff[diff['Molecule1_external']!=diff['Molecule1_internal']]
    return diff['Molecule']
def dosage_forms_not_integrated(orig,after_join):
    moltest1=pd.DataFrame(orig['GMD Dosage Form'].unique())
    moltest2=pd.DataFrame(after_join['GMD Dosage Form'].unique())
    moltest1.columns=['Dosage Form']
    moltest1['Dosage Form1']=moltest1['Dosage Form']
    moltest2.columns=['Dosage Form']
    moltest2['Dosage Form1']=moltest2['Dosage Form']
    diff=moltest1.merge(moltest2,how='left',suffixes=('_internal','_external'),on=('Dosage Form'))
    diff=diff[diff['Dosage Form1_external']!=diff['Dosage Form1_internal']]
    return diff['Dosage Form']


    