import sys
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd

patternName = (sys.argv[1])
patternName = patternName.replace("<=", "≤")
patternName = patternName.replace(">=", "≥")
originalPattern = patternName
patternName = patternName.replace(")", "").replace("(", "")
originalPatternWithoutParenthesis = patternName
patternName = patternName.split("AND")
database = (sys.argv[2])
targetAttribute = (sys.argv[3])
targetAttribute = targetAttribute.replace("<=", "≤")
targetAttribute = targetAttribute.replace(">=", "≥")
targetAttribute = targetAttribute.replace(")", "")
targetAttribute = targetAttribute.replace("(", "")
targetAttributeArray = targetAttribute.split("AND")
patternSize = len(patternName)
df = pd.read_csv(database)

print(patternName)
print(targetAttribute)
print(originalPattern)
print(originalPatternWithoutParenthesis)
print(patternSize)
print(database)

def opposite(pattern):
    if "≤" in pattern:
        pattern = pattern.replace("≤", ">")
    elif "≥" in pattern:
        pattern = pattern.replace("≥", "<")
    elif ">" in pattern:
        pattern = pattern.replace(">", "≤")
    elif "<" in pattern:
        pattern = pattern.replace("<", "≥")
    return pattern

def generatePatternPage(pattern, patternSize, df, targetAttributeArray, wholePatternWithParenthesis, wholePattern):

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
        elif len(item.split("≥")) == 2 or len(item.split("≤")) == 2:
            for sep in ["≥", "≤"]:
                if len(item.split(sep)) == 2:
                    separation = item.split(sep)
                    separator.append(sep)
                    differents.append(None)
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
        elif len(targetAttribute.split("≤")) == 2 or len(targetAttribute.split("≥")) == 2:
            for sep in ["≥", "≤"]:
                if len(targetAttribute.split(sep)) == 2:
                    ClassDiff.append(None)
                    separation = targetAttribute.split(sep)
                    ClassAttr.append(separation[0].strip())
                    ClassValue.append(separation[1].strip().replace("'",""))
                    ClassSeparator.append(sep)
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
            df[" "] =  [ "Missing" if comparedData != comparedData else str(attr[0]+" = "+value[0]) if comparedData == value[0] else str(attr[0]+" != "+value[0]) for comparedData in df[attr[0]]]
            df[attr[0]] = df[attr[0]].copy()
            df[attr[0]+str(0)] = [ "Missing" if comparedData != comparedData else str(attr[0]+" = "+value[0]) if comparedData == value[0] else str(attr[0]+" != "+value[0]) for comparedData in df[attr[0]]]
        else:
            if separator[0] == "≤":
                df[" "] =  df[attr[0]].map(lambda x : "Missing" if x != x else pattern[0] if x <= float(value[0].replace(",",".")) else opposite(pattern[0]) )
                df[attr[0]] = df[attr[0]].copy()
                df[attr[0]+str(0)] =  df[attr[0]].map(lambda x : "Missing" if x != x else pattern[0] if x <= float(value[0].replace(",",".")) else opposite(pattern[0]) )
            elif separator[0] == "<":
                df[" "] =  df[attr[0]].map(lambda x : "Missing" if x != x else pattern[0] if x < float(value[0].replace(",",".")) else opposite(pattern[0]) )
                df[attr[0]] = df[attr[0]].copy()
                df[attr[0]+str(0)] =  df[attr[0]].map(lambda x : "Missing" if x != x else pattern[0] if x < float(value[0].replace(",",".")) else opposite(pattern[0]) )
            elif separator[0] == "≥":
                df[" "] =  df[attr[0]].map(lambda x : "Missing" if x != x else pattern[0] if x >= float(value[0].replace(",",".")) else opposite(pattern[0]) )
                df[attr[0]] = df[attr[0]].copy()
                df[attr[0]+str(0)] =  df[attr[0]].map(lambda x : "Missing" if x != x else pattern[0] if x >= float(value[0].replace(",",".")) else opposite(pattern[0]) )
            else:
                df[" "] =  df[attr[0]].map(lambda x : "Missing" if x != x else pattern[0] if x > float(value[0].replace(",",".")) else opposite(pattern[0]) )
                df[attr[0]] = df[attr[0]].copy()
                df[attr[0]+str(0)] =  df[attr[0]].map(lambda x : "Missing" if x != x else pattern[0] if x > float(value[0].replace(",",".")) else opposite(pattern[0]) )
    else:
        if differents[0] != None:
            df[" "] =  [ str(attr[0]+" = "+value[0]) if comparedData == value[0] else str(attr[0]+" != "+value[0]) for comparedData in df[attr[0]]]
            df[attr[0]] = df[attr[0]].copy()
            df[attr[0]+str(0)] = [str(attr[0]+" = "+value[0]) if comparedData == value[0] else str(attr[0]+" != "+value[0]) for comparedData in df[attr[0]]]
        else:
            if separator[0] == "≤":
                df[" "] =  df[attr[0]].map(lambda x : pattern[0] if x <= float(value[0].replace(",",".")) else opposite(pattern[0]) )
                df[attr[0]] = df[attr[0]].copy()
                df[attr[0]+str(0)] =  df[attr[0]].map(lambda x : pattern[0] if x <= float(value[0].replace(",",".")) else opposite(pattern[0]) )
            elif separator[0] == "<":
                df[" "] =  df[attr[0]].map(lambda x : pattern[0] if x < float(value[0].replace(",",".")) else opposite(pattern[0]) )
                df[attr[0]] = df[attr[0]].copy()
                df[attr[0]+str(0)] =  df[attr[0]].map(lambda x : pattern[0] if x < float(value[0].replace(",",".")) else opposite(pattern[0]) )
            elif separator[0] == "≥":
                df[" "] =  df[attr[0]].map(lambda x : pattern[0] if x >= float(value[0].replace(",",".")) else opposite(pattern[0]) )
                df[attr[0]] = df[attr[0]].copy()
                df[attr[0]+str(0)] =  df[attr[0]].map(lambda x : pattern[0] if x >= float(value[0].replace(",",".")) else opposite(pattern[0]) )
            else:
                df[" "] =  df[attr[0]].map(lambda x : pattern[0] if x > float(value[0].replace(",",".")) else opposite(pattern[0]) )
                df[attr[0]] = df[attr[0]].copy()
                df[attr[0]+str(0)] =  df[attr[0]].map(lambda x : pattern[0] if x > float(value[0].replace(",",".")) else opposite(pattern[0]) )

    if patternSize > 1:
        if differents[1] != None:
            df["  "] = ["Missing" if comparedData != comparedData else comparedData  for comparedData in df[attr[1]]]
            df[attr[1]] = df[attr[1]].copy()
            df[attr[1]+str(1)] = ["Missing" if comparedData != comparedData else comparedData for comparedData in df[attr[1]]]
        else:
            if separator[1] == "≤":
                df["  "] =  df[attr[1]].map(lambda x : "Missing" if x != x else pattern[1] if x <= float(value[1].replace(",",".")) else opposite(pattern[1]) )
                df[attr[1]] = df[attr[1]].copy()
                df[attr[1]+str(1)] =  df[attr[1]].map(lambda x : "Missing" if x != x else pattern[1] if x <= float(value[1].replace(",",".")) else opposite(pattern[1]) )
            elif separator[1] == "<":
                df["  "] =  df[attr[1]].map(lambda x : "Missing" if x != x else pattern[1] if x < float(value[1].replace(",",".")) else opposite(pattern[1]) )
                df[attr[1]] = df[attr[1]].copy()
                df[attr[1]+str(1)] =  df[attr[1]].map(lambda x : "Missing" if x != x else pattern[1] if x < float(value[1].replace(",",".")) else opposite(pattern[1]) )
            elif separator[1] == "≥":
                df["  "] =  df[attr[1]].map(lambda x : "Missing" if x != x else pattern[1] if x >= float(value[1].replace(",",".")) else opposite(pattern[1]) )
                df[attr[1]] = df[attr[1]].copy()
                df[attr[1]+str(1)] =  df[attr[1]].map(lambda x : "Missing" if x != x else pattern[1] if x >= float(value[1].replace(",",".")) else opposite(pattern[1]) )
            else:
                df["  "] =  df[attr[1]].map(lambda x : "Missing" if x != x else pattern[1] if x > float(value[1].replace(",",".")) else opposite(pattern[1]) )
                df[attr[1]] = df[attr[1]].copy()
                df[attr[1]+str(1)] =  df[attr[1]].map(lambda x : "Missing" if x != x else pattern[1] if x > float(value[1].replace(",",".")) else opposite(pattern[1]) )

    if patternSize > 2:
        if differents[2] != None:
            df["   "] =  [ str(attr[2]+" = "+value[2]) if comparedData == value[2] else str(attr[2]+" != "+value[2]) for comparedData in df[attr[2]]]
            df[attr[2]] = df[attr[2]].copy()
            df[attr[2]+str(2)] = [ str(attr[2]+" = "+value[2]) if comparedData == value[2] else str(attr[2]+" != "+value[2]) for comparedData in df[attr[2]]]
        else:
            if separator[2] == "≤":
                df["   "] =  df[attr[2]].map(lambda x : pattern[2] if x <= float(value[2].replace(",",".")) else opposite(pattern[2]) )
                df[attr[2]] = df[attr[2]].copy()
                df[attr[2]+str(2)] =  df[attr[2]].map(lambda x : pattern[2] if x <= float(value[2].replace(",",".")) else opposite(pattern[2]) )
            elif separator[2] == "<":
                df["   "] =  df[attr[2]].map(lambda x : pattern[2] if x < float(value[2].replace(",",".")) else opposite(pattern[2]) )
                df[attr[2]] = df[attr[2]].copy()
                df[attr[2]+str(2)] =  df[attr[2]].map(lambda x : pattern[2] if x < float(value[2].replace(",",".")) else opposite(pattern[2]) )
            elif separator[2] == "≥":
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
            if ClassSeparator[0] == "≤":
                df[column] =  df[column].map(lambda x : targetAttributeArray[0] if x <= float(ClassValue[0].replace(",",".")) else opposite(targetAttributeArray[0]))
            elif ClassSeparator[0] == "<":
                df[column] =  df[column].map(lambda x : targetAttributeArray[0] if x < float(ClassValue[0].replace(",",".")) else opposite(targetAttributeArray[0]))
            elif ClassSeparator[0] == "≥":
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
                if ClassSeparator[1] == "≤":
                    if ClassDiff[0]:
                        df[className] =  [ className if comparedData0 == ClassValue[0] and comparedData1 <= float(ClassValue[1].replace(",", ".")) else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
                    else:
                        df[className] =  [ className if comparedData0 != ClassValue[0] and comparedData1 <= float(ClassValue[1].replace(",", ".")) else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
                elif ClassSeparator[1] == "<":
                    if ClassDiff[0]:
                        df[className] =  [ className if comparedData0 == ClassValue[0] and comparedData1 < float(ClassValue[1].replace(",", ".")) else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
                    else:
                        df[className] =  [ className if comparedData0 != ClassValue[0] and comparedData1 < float(ClassValue[1].replace(",", ".")) else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
                elif ClassSeparator[1] == "≥":
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
            if ClassSeparator[0] == "≤":
                if ClassDiff[1] != None:
                    if ClassDiff[1]:
                        df[className] =  [ className if comparedData1 == ClassValue[1] and comparedData0 <= float(ClassValue[0].replace(",", ".")) else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
                    else:
                        df[className] =  [ className if comparedData1 != ClassValue[1] and comparedData0 <= float(ClassValue[0].replace(",", ".")) else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
                else:
                    if ClassSeparator[1] == "≤":
                        df[className] =  [ className if comparedData0 <= float(ClassValue[0].replace(",", ".")) and comparedData1 <= float(ClassValue[1].replace(",", ".")) else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
                    elif ClassSeparator[1] == "<":
                        df[className] =  [ className if comparedData0 <= float(ClassValue[0].replace(",", ".")) and comparedData1 < float(ClassValue[1].replace(",", ".")) else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
                    elif ClassSeparator[1] == "≥":
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
                    if ClassSeparator[1] == "≤":
                        df[className] =  [ className if comparedData0 < float(ClassValue[0].replace(",", ".")) and comparedData1 <= float(ClassValue[1].replace(",", ".")) else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
                    elif ClassSeparator[1] == "<":
                        df[className] =  [ className if comparedData0 < float(ClassValue[0].replace(",", ".")) and comparedData1 < float(ClassValue[1].replace(",", ".")) else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
                    elif ClassSeparator[1] == "≥":
                        df[className] =  [ className if comparedData0 < float(ClassValue[0].replace(",", ".")) and comparedData1 >= float(ClassValue[1].replace(",", ".")) else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
                    else:
                        df[className] =  [ className if comparedData0 < float(ClassValue[0].replace(",", ".")) and comparedData1 > float(ClassValue[1].replace(",", ".")) else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
            elif ClassSeparator[0] == "≥":
                if ClassDiff[1] != None:
                    if ClassDiff[1]:
                        df[className] =  [ className if comparedData1 == ClassValue[1] and comparedData0 >= float(ClassValue[0].replace(",", ".")) else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
                    else:
                        df[className] =  [ className if comparedData1 != ClassValue[1] and comparedData0 >= float(ClassValue[0].replace(",", ".")) else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
                else:
                    if ClassSeparator[1] == "≤":
                        df[className] =  [ className if comparedData0 >= float(ClassValue[0].replace(",", ".")) and comparedData1 <= float(ClassValue[1].replace(",", ".")) else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
                    elif ClassSeparator[1] == "<":
                        df[className] =  [ className if comparedData0 >= float(ClassValue[0].replace(",", ".")) and comparedData1 < float(ClassValue[1].replace(",", ".")) else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
                    elif ClassSeparator[1] == "≥":
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
                    if ClassSeparator[1] == "≤":
                        df[className] =  [ className if comparedData0 > float(ClassValue[0].replace(",", ".")) and comparedData1 <= float(ClassValue[1].replace(",", ".")) else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
                    elif ClassSeparator[1] == "<":
                        df[className] =  [ className if comparedData0 > float(ClassValue[0].replace(",", ".")) and comparedData1 < float(ClassValue[1].replace(",", ".")) else "NOT ("+className+")" for comparedData0, comparedData1 in zip(df[column0], df[column1])]
                    elif ClassSeparator[1] == "≥":
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
        title = "IF {"+wholePatternWithParenthesis+"} THEN {("+targetAttributeArray[0]+")}"
    else:
        title = "IF {"+wholePatternWithParenthesis+"} THEN {("+targetAttributeArray[0]+") AND ("+targetAttributeArray[1]+")}"
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

        fig.write_html('index.html', auto_open=True)
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

        fig.write_html('index.html', auto_open=True)


generatePatternPage(patternName, patternSize, df, targetAttributeArray, originalPattern, originalPatternWithoutParenthesis)