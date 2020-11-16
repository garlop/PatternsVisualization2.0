import sys
import dominate
from dominate.tags import *
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import webbrowser

patternName = (sys.argv[1])
originalPattern = patternName
patternName = patternName.split("AND")
database = (sys.argv[2])
targetAttribute = (sys.argv[3])
targetAttributeArray = targetAttribute.split("AND")
patternSize = len(patternName)
df = pd.read_csv(database)

def opposite(pattern):
    if "=" in pattern:
        if "<" in pattern:
            pattern = pattern.replace("<=", ">")
        elif ">" in pattern:
            pattern = pattern.replace(">=", "<")
    else:
        if ">" in pattern:
            pattern = pattern.replace(">", "<=")
        elif "<" in pattern:
            pattern = pattern.replace("<", ">=")
    return pattern

def generatePatternPage(pattern, patternSize, df, targetAttributeArray, wholePattern):

    attr = []
    value = []
    separator = []
    differents = []
    for item in pattern:
        different = None
        if len(item.split("!=")) == 2:
            separation = item.split("!=")
            differents.append(True)
            attr.append(separation[0].strip())
            value.append(separation[1].strip().replace("'",""))
            separator.append("!=")
        elif len(item.split("=")) == 2:
            separation = item.split("=")
            differents.append(False)
            attr.append(separation[0].strip())
            value.append(separation[1].strip().replace("'",""))
            separator.append("=")
            for sep in [">=", "<="]:
                if len(item.split(sep)) == 2:
                    separator.append(sep)
                    differents[-1] = None
                    attr.remove(separation[0].strip())
                    value.remove(separation[1].strip())
                    separator.remove("=")
                    separation = item.split(sep)
                    attr.append(separation[0].strip())
                    value.append(separation[1].strip().replace("'",""))
                    separator.append(sep)
        else:
            for sep in [">", "<"]:
                if len(item.split(sep)) == 2:
                    separator.append(sep)
                    differents.append(None)
                    separation = item.split(sep)
                    attr.append(separation[0].strip())
                    value.append(separation[1].strip().replace("'",""))
    
    ClassDiff = []
    ClassAttr = []
    ClassValue = []
    ClassSeparator = []

    for targetAttribute in targetAttributeArray:
        if len(targetAttribute.split("!=")) == 2:
            separation = targetAttribute.split("!=")
            ClassDiff.append(True)
            ClassAttr.append(separation[0].strip())
            ClassValue.append(separation[1].strip().replace("'",""))
            ClassSeparator.append("!=")
        elif len(targetAttribute.split("=")) == 2:
            separation = targetAttribute.split("=")
            ClassDiff.append(False)
            ClassAttr.append(separation[0].strip())
            ClassValue.append(separation[1].strip().replace("'",""))
            ClassSeparator.append("=")
            for sep in [">=", "<="]:
                if len(targetAttribute.split(sep)) == 2:
                    ClassDiff[-1] = None
                    separation = targetAttribute.split(sep)
                    ClassAttr[-1] = separation[0].strip()
                    ClassValue[-1] = separation[1].strip().replace("'","")
                    ClassSeparator[-1] = sep
        else:
            for sep in [">", "<"]:
                if len(targetAttribute.split(sep)) == 2:
                    ClassSeparator.append(sep)
                    ClassDiff.append(None)
                    separation = targetAttribute.split(sep)
                    ClassAttr.append(separation[0].strip())
                    ClassValue.append(separation[1].strip().replace("'",""))

    if patternSize == 1:
        if differents[0] != None:
            df[" "] =  [ "Missing" if comparedData != comparedData else str(value[0]) if comparedData == value[0] else "Not "+str(value[0]) for comparedData in df[attr[0]]]
            df[attr[0]] = df[attr[0]].copy()
            df[attr[0]+str(0)] = [ "Missing" if comparedData != comparedData else str(value[0]) if comparedData == value[0] else "Not "+str(value[0]) for comparedData in df[attr[0]]]
        else:
            if separator[0] == "<=":
                df[" "] =  df[attr[0]].map(lambda x : "Missing" if x != x else pattern[0] if x <= float(value[0].replace(",",".")) else opposite(pattern[0]) )
                df[attr[0]] = df[attr[0]].copy()
                df[attr[0]+str(0)] =  df[attr[0]].map(lambda x : "Missing" if x != x else pattern[0] if x <= float(value[0].replace(",",".")) else opposite(pattern[0]) )
            elif separator[0] == "<":
                df[" "] =  df[attr[0]].map(lambda x : "Missing" if x != x else pattern[0] if x < float(value[0].replace(",",".")) else opposite(pattern[0]) )
                df[attr[0]] = df[attr[0]].copy()
                df[attr[0]+str(0)] =  df[attr[0]].map(lambda x : "Missing" if x != x else pattern[0] if x < float(value[0].replace(",",".")) else opposite(pattern[0]) )
            elif separator[0] == ">=":
                df[" "] =  df[attr[0]].map(lambda x : "Missing" if x != x else pattern[0] if x >= float(value[0].replace(",",".")) else opposite(pattern[0]) )
                df[attr[0]] = df[attr[0]].copy()
                df[attr[0]+str(0)] =  df[attr[0]].map(lambda x : "Missing" if x != x else pattern[0] if x >= float(value[0].replace(",",".")) else opposite(pattern[0]) )
            else:
                df[" "] =  df[attr[0]].map(lambda x : "Missing" if x != x else pattern[0] if x > float(value[0].replace(",",".")) else opposite(pattern[0]) )
                df[attr[0]] = df[attr[0]].copy()
                df[attr[0]+str(0)] =  df[attr[0]].map(lambda x : "Missing" if x != x else pattern[0] if x > float(value[0].replace(",",".")) else opposite(pattern[0]) )
    else:
        if differents[0] != None:
            df[" "] =  [ str(value[0]) if comparedData == value[0] else "Not "+str(value[0]) for comparedData in df[attr[0]]]
            df[attr[0]] = df[attr[0]].copy()
            df[attr[0]+str(0)] = [str(value[0]) if comparedData == value[0] else "Not "+str(value[0]) for comparedData in df[attr[0]]]
        else:
            if separator[0] == "<=":
                df[" "] =  df[attr[0]].map(lambda x : pattern[0] if x <= float(value[0].replace(",",".")) else opposite(pattern[0]) )
                df[attr[0]] = df[attr[0]].copy()
                df[attr[0]+str(0)] =  df[attr[0]].map(lambda x : pattern[0] if x <= float(value[0].replace(",",".")) else opposite(pattern[0]) )
            elif separator[0] == "<":
                df[" "] =  df[attr[0]].map(lambda x : pattern[0] if x < float(value[0].replace(",",".")) else opposite(pattern[0]) )
                df[attr[0]] = df[attr[0]].copy()
                df[attr[0]+str(0)] =  df[attr[0]].map(lambda x : pattern[0] if x < float(value[0].replace(",",".")) else opposite(pattern[0]) )
            elif separator[0] == ">=":
                df[" "] =  df[attr[0]].map(lambda x : pattern[0] if x >= float(value[0].replace(",",".")) else opposite(pattern[0]) )
                df[attr[0]] = df[attr[0]].copy()
                df[attr[0]+str(0)] =  df[attr[0]].map(lambda x : pattern[0] if x >= float(value[0].replace(",",".")) else opposite(pattern[0]) )
            else:
                df[" "] =  df[attr[0]].map(lambda x : pattern[0] if x > float(value[0].replace(",",".")) else opposite(pattern[0]) )
                df[attr[0]] = df[attr[0]].copy()
                df[attr[0]+str(0)] =  df[attr[0]].map(lambda x : pattern[0] if x > float(value[0].replace(",",".")) else opposite(pattern[0]) )

    if patternSize > 1:
        if differents[1] != None:
            df["  "] = ["Missing" if comparedData != comparedData else comparedData for comparedData in df[attr[1]]]
            df[attr[1]] = df[attr[1]].copy()
            df[attr[1]+str(1)] = ["Missing" if comparedData != comparedData else comparedData for comparedData in df[attr[1]]]
        else:
            if separator[1] == "<=":
                df["  "] =  df[attr[1]].map(lambda x : "Missing" if x != x else pattern[1] if x <= float(value[1].replace(",",".")) else opposite(pattern[1]) )
                df[attr[1]] = df[attr[1]].copy()
                df[attr[1]+str(1)] =  df[attr[1]].map(lambda x : "Missing" if x != x else pattern[1] if x <= float(value[1].replace(",",".")) else opposite(pattern[1]) )
            elif separator[1] == "<":
                df["  "] =  df[attr[1]].map(lambda x : "Missing" if x != x else pattern[1] if x < float(value[1].replace(",",".")) else opposite(pattern[1]) )
                df[attr[1]] = df[attr[1]].copy()
                df[attr[1]+str(1)] =  df[attr[1]].map(lambda x : "Missing" if x != x else pattern[1] if x < float(value[1].replace(",",".")) else opposite(pattern[1]) )
            elif separator[1] == ">=":
                df["  "] =  df[attr[1]].map(lambda x : "Missing" if x != x else pattern[1] if x >= float(value[1].replace(",",".")) else opposite(pattern[1]) )
                df[attr[1]] = df[attr[1]].copy()
                df[attr[1]+str(1)] =  df[attr[1]].map(lambda x : "Missing" if x != x else pattern[1] if x >= float(value[1].replace(",",".")) else opposite(pattern[1]) )
            else:
                df["  "] =  df[attr[1]].map(lambda x : "Missing" if x != x else pattern[1] if x > float(value[1].replace(",",".")) else opposite(pattern[1]) )
                df[attr[1]] = df[attr[1]].copy()
                df[attr[1]+str(1)] =  df[attr[1]].map(lambda x : "Missing" if x != x else pattern[1] if x > float(value[1].replace(",",".")) else opposite(pattern[1]) )

    if patternSize > 2:
        if differents[2] != None:
            df["   "] =  [ str(value[2]) if comparedData == value[2] else "Not "+str(value[2]) for comparedData in df[attr[2]]]
            df[attr[2]] = df[attr[2]].copy()
            df[attr[2]+str(2)] = [ str(value[2]) if comparedData == value[2] else "Not "+str(value[2]) for comparedData in df[attr[2]]]
        else:
            if separator[2] == "<=":
                df["   "] =  df[attr[2]].map(lambda x : pattern[2] if x <= float(value[2].replace(",",".")) else opposite(pattern[2]) )
                df[attr[2]] = df[attr[2]].copy()
                df[attr[2]+str(2)] =  df[attr[2]].map(lambda x : pattern[2] if x <= float(value[2].replace(",",".")) else opposite(pattern[2]) )
            elif separator[2] == "<":
                df["   "] =  df[attr[2]].map(lambda x : pattern[2] if x < float(value[2].replace(",",".")) else opposite(pattern[2]) )
                df[attr[2]] = df[attr[2]].copy()
                df[attr[2]+str(2)] =  df[attr[2]].map(lambda x : pattern[2] if x < float(value[2].replace(",",".")) else opposite(pattern[2]) )
            elif separator[2] == ">=":
                df["   "] =  df[attr[2]].map(lambda x : pattern[2] if x >= float(value[2].replace(",",".")) else opposite(pattern[2]) )
                df[attr[2]] = df[attr[2]].copy()
                df[attr[2]+str(2)] =  df[attr[2]].map(lambda x : pattern[2] if x >= float(value[2].replace(",",".")) else opposite(pattern[2]) )
            else:
                df["   "] =  df[attr[2]].map(lambda x : pattern[2] if x > float(value[2].replace(",",".")) else opposite(pattern[2]) )
                df[attr[2]] = df[attr[2]].copy()
                df[attr[2]+str(2)] =  df[attr[2]].map(lambda x : pattern[2] if x > float(value[2].replace(",",".")) else opposite(pattern[2]) )

    attributes = []

    if len(targetAttributeArray) == 1:
        column = ClassAttr[0]

        if ClassDiff[0] != None:
            df[column] = ["Missing" if comparedData != comparedData else comparedData for comparedData in df[column]]        
        else:
            if ClassSeparator[0] == "<=":
                df[column] =  df[column].map(lambda x : targetAttributeArray[0] if x <= float(ClassValue[0].replace(",",".")) else opposite(targetAttributeArray[0]))
            elif ClassSeparator[0] == "<":
                df[column] =  df[column].map(lambda x : targetAttributeArray[0] if x < float(ClassValue[0].replace(",",".")) else opposite(targetAttributeArray[0]))
            elif ClassSeparator[0] == ">=":
                df[column] =  df[column].map(lambda x : targetAttributeArray[0] if x >= float(ClassValue[0].replace(",",".")) else opposite(targetAttributeArray[0]))
            else:
                df[column] =  df[column].map(lambda x : targetAttributeArray[0] if x > float(ClassValue[0].replace(",",".")) else opposite(targetAttributeArray[0]))
        attributes = [attr[i]+str(i) for i in range(len(attr))]
        attributes.append(column)
    else:

        column0 = ClassAttr[0]
        column1 = ClassAttr[1]

        className = targetAttributeArray[0]+" AND "+targetAttributeArray[1]
        if ClassDiff[0] != None:
            if ClassDiff[1] != None:
                if ClassDiff[0]:
                    if ClassDiff[1]:
                        df[className] = [ className if comparedData0 == ClassValue[0] and comparedData1 == ClassValue[1] else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
                    else:
                        df[className] = [ className if comparedData0 == ClassValue[0] and comparedData1 != ClassValue[1] else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
                else:
                    if ClassDiff[1]:
                        df[className] = [ className if comparedData0 != ClassValue[0] and comparedData1 == ClassValue[1] else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
                    else:
                        df[className] = [ className if comparedData0 != ClassValue[0] and comparedData1 != ClassValue[1] else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
            else:
                if ClassSeparator[1] == "<=":
                    if ClassDiff[0]:
                        df[className] =  [ className if comparedData0 == ClassValue[0] and comparedData1 <= float(ClassValue[1].replace(",", ".")) else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
                    else:
                        df[className] =  [ className if comparedData0 != ClassValue[0] and comparedData1 <= float(ClassValue[1].replace(",", ".")) else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
                elif ClassSeparator[1] == "<":
                    if ClassDiff[0]:
                        df[className] =  [ className if comparedData0 == ClassValue[0] and comparedData1 < float(ClassValue[1].replace(",", ".")) else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
                    else:
                        df[className] =  [ className if comparedData0 != ClassValue[0] and comparedData1 < float(ClassValue[1].replace(",", ".")) else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
                elif ClassSeparator[1] == ">=":
                    if ClassDiff[0]:
                        df[className] =  [ className if comparedData0 == ClassValue[0] and comparedData1 >= float(ClassValue[1].replace(",", ".")) else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
                    else:
                        df[className] =  [ className if comparedData0 != ClassValue[0] and comparedData1 >= float(ClassValue[1].replace(",", ".")) else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
                else:
                    if ClassDiff[0]:
                        df[className] =  [ className if comparedData0 == ClassValue[0] and comparedData1 > float(ClassValue[1].replace(",", ".")) else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
                    else:
                        df[className] =  [ className if comparedData0 != ClassValue[0] and comparedData1 > float(ClassValue[1].replace(",", ".")) else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]  
        else:
            if ClassSeparator[0] == "<=":
                if ClassDiff[1] != None:
                    if ClassDiff[1]:
                        df[className] =  [ className if comparedData1 == ClassValue[1] and comparedData0 <= float(ClassValue[0].replace(",", ".")) else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
                    else:
                        df[className] =  [ className if comparedData1 != ClassValue[1] and comparedData0 <= float(ClassValue[0].replace(",", ".")) else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
                else:
                    if ClassSeparator[1] == "<=":
                        df[className] =  [ className if comparedData0 <= float(ClassValue[0].replace(",", ".")) and comparedData1 <= float(ClassValue[1].replace(",", ".")) else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
                    elif ClassSeparator[1] == "<":
                        df[className] =  [ className if comparedData0 <= float(ClassValue[0].replace(",", ".")) and comparedData1 < float(ClassValue[1].replace(",", ".")) else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
                    elif ClassSeparator[1] == ">=":
                        df[className] =  [ className if comparedData0 <= float(ClassValue[0].replace(",", ".")) and comparedData1 >= float(ClassValue[1].replace(",", ".")) else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
                    else:
                        df[className] =  [ className if comparedData0 <= float(ClassValue[0].replace(",", ".")) and comparedData1 > float(ClassValue[1].replace(",", ".")) else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
            elif ClassSeparator[0] == "<":
                if ClassDiff[1] != None:
                    if ClassDiff[1]:
                        df[className] =  [ className if comparedData1 == ClassValue[1] and comparedData0 < float(ClassValue[0].replace(",", ".")) else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
                    else:
                        df[className] =  [ className if comparedData1 != ClassValue[1] and comparedData0 < float(ClassValue[0].replace(",", ".")) else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
                else:
                    if ClassSeparator[1] == "<=":
                        df[className] =  [ className if comparedData0 < float(ClassValue[0].replace(",", ".")) and comparedData1 <= float(ClassValue[1].replace(",", ".")) else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
                    elif ClassSeparator[1] == "<":
                        df[className] =  [ className if comparedData0 < float(ClassValue[0].replace(",", ".")) and comparedData1 < float(ClassValue[1].replace(",", ".")) else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
                    elif ClassSeparator[1] == ">=":
                        df[className] =  [ className if comparedData0 < float(ClassValue[0].replace(",", ".")) and comparedData1 >= float(ClassValue[1].replace(",", ".")) else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
                    else:
                        df[className] =  [ className if comparedData0 < float(ClassValue[0].replace(",", ".")) and comparedData1 > float(ClassValue[1].replace(",", ".")) else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
            elif ClassSeparator[0] == ">=":
                if ClassDiff[1] != None:
                    if ClassDiff[1]:
                        df[className] =  [ className if comparedData1 == ClassValue[1] and comparedData0 >= float(ClassValue[0].replace(",", ".")) else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
                    else:
                        df[className] =  [ className if comparedData1 != ClassValue[1] and comparedData0 >= float(ClassValue[0].replace(",", ".")) else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
                else:
                    if ClassSeparator[1] == "<=":
                        df[className] =  [ className if comparedData0 >= float(ClassValue[0].replace(",", ".")) and comparedData1 <= float(ClassValue[1].replace(",", ".")) else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
                    elif ClassSeparator[1] == "<":
                        df[className] =  [ className if comparedData0 >= float(ClassValue[0].replace(",", ".")) and comparedData1 < float(ClassValue[1].replace(",", ".")) else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
                    elif ClassSeparator[1] == ">=":
                        df[className] =  [ className if comparedData0 >= float(ClassValue[0].replace(",", ".")) and comparedData1 >= float(ClassValue[1].replace(",", ".")) else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
                    else:
                        df[className] =  [ className if comparedData0 >= float(ClassValue[0].replace(",", ".")) and comparedData1 > float(ClassValue[1].replace(",", ".")) else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
            else:
                if ClassDiff[1] != None:
                    if ClassDiff[1]:
                        df[className] =  [ className if comparedData1 == ClassValue[1] and comparedData0 > float(ClassValue[0].replace(",", ".")) else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
                    else:
                        df[className] =  [ className if comparedData1 != ClassValue[1] and comparedData0 > float(ClassValue[0].replace(",", ".")) else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
                else:
                    if ClassSeparator[1] == "<=":
                        df[className] =  [ className if comparedData0 > float(ClassValue[0].replace(",", ".")) and comparedData1 <= float(ClassValue[1].replace(",", ".")) else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
                    elif ClassSeparator[1] == "<":
                        df[className] =  [ className if comparedData0 > float(ClassValue[0].replace(",", ".")) and comparedData1 < float(ClassValue[1].replace(",", ".")) else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
                    elif ClassSeparator[1] == ">=":
                        df[className] =  [ className if comparedData0 > float(ClassValue[0].replace(",", ".")) and comparedData1 >= float(ClassValue[1].replace(",", ".")) else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
                    else:
                        df[className] =  [ className if comparedData0 > float(ClassValue[0].replace(",", ".")) and comparedData1 > float(ClassValue[1].replace(",", ".")) else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]

        attributes = [attr[i]+str(i) for i in range(len(attr))]
        attributes.append(className)    

    attributes.append(" ")
    if patternSize > 1:
        attributes.append("  ")
    if patternSize > 2:
        attributes.append("   ")

    dfpattern = df.groupby(attributes).size().reset_index().rename(columns={0:'count'})
    
    print(dfpattern)

    for j in range(len(attr)):
        if attr[j] != None:
            #5 main values
            count = dfpattern.groupby(attr[j]+str(j))[attr[j]+str(j)].nunique()
            count = len(count)
            if(count > 5):
                dfpattern = dfpattern.sort_values(by = ['count'], ascending=False).reset_index()
                fields = set()
                i = 0
                fields.add(value[j])
                while len(fields) < 4:
                    if dfpattern[attr[j]+str(j)][i] != "Missing":
                        fields.add(dfpattern[attr[j]+str(j)][i])
                    i = i+1

                dfpattern[" "*(j+1)] = [val if val in fields else "Other" for val in dfpattern[attr[j]]]
                dfpattern[attr[j]+str(j)] = [val if val in fields else "Other" for val in dfpattern[attr[j]]]

    if len(targetAttributeArray) == 1:
        if ClassDiff[0] != None:
            #5 main values
            count = dfpattern.groupby(ClassAttr[0])[ClassAttr[0]].nunique()
            count = len(count)
            if(count > 5):
                dfpattern = dfpattern.sort_values(by = ['count'], ascending=False).reset_index()
                fields = set()
                i = 0
                fields.add(ClassValue[0])
                while len(fields) < 4:
                    if dfpattern[ClassAttr[0]][i] != "Missing":
                        fields.add(dfpattern[ClassAttr[0]][i])
                    i = i+1
                dfpattern[ClassAttr[0]] = [val if val in fields else "Other" for val in dfpattern[ClassAttr[0]]]

        attributes = [attr[i]+str(i) for i in range(len(attr))]
        attributes.append(ClassAttr[0])

    attributes.append(" ")
    if patternSize > 1:
        attributes.append("  ")
    if patternSize > 2:
        attributes.append("   ")

    print(dfpattern)

    try:
        dfpattern = dfpattern.groupby(attributes)['count'].sum().reset_index().rename(columns={0:'count'})
    except:
        pass

    title = ""
    if len(targetAttributeArray) == 1:
        title = "IF ("+wholePattern+") THEN ("+targetAttributeArray[0]+")"
    else:
        title = "IF ("+wholePattern+") THEN ("+targetAttributeArray[0]+" AND "+targetAttributeArray[1]+")"
    size = 1638//len(title)

    fig = None

    if len(targetAttributeArray) == 1:
        if patternSize > 2:
            fig = px.bar(dfpattern, x=ClassAttr[0], y="count", color=attr[1]+str(1), barmode="group",
                facet_row="   ", facet_col=" ",
                category_orders={attr[2]: [value[2]],
                                attr[0]: [value[0]]})
            fig.update_layout(title={
                'text': title,
                'font_size' : size,
                'y':1.0,
                'x':0.5}, legend=dict(
                title=attr[1], orientation="v", y=0.5, yanchor="top"
            ))
        elif patternSize > 1:
            fig = px.bar(dfpattern, x=ClassAttr[0], y="count", color=attr[1]+str(1), barmode="group",
                facet_col=" ",
                category_orders={attr[0]: [value[0]]})
            fig.update_layout(title={
                'text': title,
                'font_size' : size,
                'y':1.0,
                'x':0.5}, legend=dict(
                title=attr[1], orientation="v", y=0.5, yanchor="top"
            ))
        else:
            fig = px.bar(dfpattern, x=ClassAttr[0], y="count", color=attr[0]+str(0), barmode="group")
            fig.update_layout(title={
                'text': title,
                'font_size' : size,
                'y':1.0,
                'x':0.5}, legend=dict(
                title=attr[0], orientation="v", y=0.5, yanchor="top"
            ))

        fig.write_html('graph.html', default_width='100%', default_height='100%')
    else:
        if patternSize > 2:
            fig = px.bar(dfpattern, x=className, y="count", color=attr[1]+str(1), barmode="group",
                facet_row="   ", facet_col=" ",
                category_orders={attr[2]: [value[2]],
                                attr[0]: [value[0]]})
            fig.update_layout(title={
                'text': title,
                'font_size' : size,
                'y':1.0,
                'x':0.5}, legend=dict(
                title=attr[1], orientation="v", y=0.5, yanchor="top"
            ))
        elif patternSize > 1:
            fig = px.bar(dfpattern, x=className, y="count", color=attr[1]+str(1), barmode="group",
                facet_col=" ",
                category_orders={attr[0]: [value[0]]})
            fig.update_layout(title={
                'text': title,
                'font_size' : size,
                'y':1.0,
                'x':0.5}, legend=dict(
                title=attr[1], orientation="v", y=0.5, yanchor="top"
            ))
        else:
            fig = px.bar(dfpattern, x=className, y="count", color=attr[0]+str(0), barmode="group")
            fig.update_layout(title={
                'text': title,
                'font_size' : size,
                'y':1.0,
                'x':0.5}, legend=dict(
                title=attr[0], orientation="v", y=0.5, yanchor="top"
            ))

        fig.write_html('graph.html', default_width='100%', default_height='100%')


#        if separador == "<=":
#            dfpattern[" "] =  dfpattern[field].map(lambda x : 'Item compliant' if x <= float(value.replace(",",".")) else 'Not Item compliant')
#            dfpattern[field] =  dfpattern[field].map(lambda x : pattern if x <= float(value.replace(",",".")) else opposite(pattern) )
#            dfpattern = dfpattern.groupby([" " , field, targetAttribute]).size().reset_index().rename(columns={0:'count'})
#        elif separador == "<":
#            dfpattern[" "] =  dfpattern[field].map(lambda x : 'Item compliant' if x < float(value.replace(",",".")) else 'Not Item compliant' )
#            dfpattern[field] =  dfpattern[field].map(lambda x : pattern if x < float(value.replace(",",".")) else opposite(pattern) )
#            dfpattern = dfpattern.groupby([" " , field, targetAttribute]).size().reset_index().rename(columns={0:'count'})
#        elif separador == ">=":
#            dfpattern[" "] =  dfpattern[field].map(lambda x : 'Item compliant' if x >= float(value.replace(",",".")) else 'Not Item compliant' )
#            dfpattern[field] =  dfpattern[field].map(lambda x : pattern if x >= float(value.replace(",",".")) else opposite(pattern) )
#            dfpattern = dfpattern.groupby([" " , field, targetAttribute]).size().reset_index().rename(columns={0:'count'})
#        else:
#            dfpattern[" "] =  dfpattern[field].map(lambda x : 'Item compliant' if x > float(value.replace(",",".")) else 'Not Item compliant')
#            dfpattern[field] =  dfpattern[field].map(lambda x : pattern if x > float(value.replace(",",".")) else opposite(pattern))
#            dfpattern = dfpattern.groupby([" " , field, targetAttribute]).size().reset_index().rename(columns={0:'count'})
    
#        dfpattern[targetAttribute] = ["|"+str(val)+"|" for val in dfpattern[targetAttribute]]

#        fig = px.bar(dfpattern, x=targetAttribute, y="count", color=field, facet_col=" ")
#        fig.update_layout(title={
#            'text': field,
#            'y':1.0,
#            'x':0.5,
#            'xanchor': 'center',
#            'yanchor': 'top'}, legend=dict(
#            title=None, orientation="h", y=1.1, yanchor="bottom", x=0.5, xanchor="center"
#        ))
#        fig.write_html(str(pageNumber)+'.html', default_width='100%', default_height='100%')


doc = dominate.document(title='Pattern Visualization')

with doc.head:
    link(rel='stylesheet', href='style.css', type='text/css')
    script(src='https://code.jquery.com/jquery-3.5.1.js', integrity='sha256-QWo7LDvxbWT2tbbQ97B53yJnYU3WhH/C8ycbRAkjPDc=', crossorigin='anonymous')

with doc:
    h1('Pattern Visualization')
    with div():
        hr()
        generatePatternPage(patternName, patternSize, df, targetAttributeArray, originalPattern)
        iframe(src="graph.html", onload="javascript:(function(o){o.style.height=o.contentWindow.document.body.scrollHeight+'px';}(this));", style="height:100%;width:70%;border:none;overflow:hidden;")

with open("index.html", "w", encoding='UTF-8') as document:
    document.write(str(doc).replace("<!DOCTYPE html>", ""))

with open("style.css", "w", encoding='UTF-8') as cssstyle:
    cssstyle.write("h1, h2, div { text-align: center; justify-content: center;} code { background: hsl(220, 80%, 90%); } pre { text-align: center; white-space: pre-wrap; background: hsl(30,80%,90%);} pre.item{width: 80%; margin-left: 10%; margin-right: 10%;}")

webbrowser.open_new_tab('index.html')