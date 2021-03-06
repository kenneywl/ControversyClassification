import pandas as pd
from math import sqrt,log
from sklearn.preprocessing import RobustScaler

#For the factors:
fa = pd.read_excel("Factors.xlsx")
fa = pd.DataFrame(fa)
fa_ndm = fa.iloc[:,2:]

print(list(fa_ndm))

'''
#######################################################################
#For the titles we don't have the result of majority voting.
#Note I used iss for "controvesial", som for "somewhat" and not for
#"not controversial". It makes the resp have the same length. Here we go:

ti = pd.read_excel("Titles.xlsx")
tsc = ti.iloc[0:1000,3]
tnc = ti.iloc[0:1000,4]
tc = ti.iloc[0:1000,2]

tcont = []
for i in range(1000):
	thr = [tc[i], tsc[i], tnc[i]]
	d = max(thr)
	if thr.count(d) > 1:
		ans = "unk"
	else:
		ind = thr.index(d)
		ans = ["Controversial","Somewhat Controversial","Not Controversial"][ind]

	tcont += [ans]

titles_r = pd.DataFrame(tcont)[0]

#columns the paper says were used for the titles:
ind = [85,50,83,94,49,33,6,61,35,7,2,8,71,63,32,10,70,37,29,4,72, \
       58,45,64,25,42,31,51,67,59,68,20]

fa = fa.iloc[:,ind]

#Note we are missing standard devation and entropy.
#Lets include them: (this might be wrong.)

#for stand dev
ssd = []
mean = 20/3
for i in range(len(tc)):
	ssd += [sqrt(tc[i]*(tc[i]-mean)**2+tsc[i]*(tsc[i]-mean)**2+tnc[i]*(tnc[i]-mean)**2)]

ssd = [i/sqrt(20) for i in ssd]

#for entropy
sen = []
for i in range(len(tc)):
	if tc[i] == 0: tc[i] = 1
	if tsc[i] == 0: tsc[i] = 1
	if tnc[i] == 0: tnc[i] = 1

	sen += [20*log(20)-(tc[i]*log(tc[i])+tsc[i]*log(tsc[i])+tnc[i]*log(tnc[i]))]

sen = [i/20 for i in sen]

titles_disp = pd.DataFrame(data={"Entropy":sen})
titles = fa

#"titles" should be the factors used for each model. titles_r should
#be the responses.
###################################################################
#For the summaries:
su = pd.read_excel("Summaries.xlsx")

scont = su.iloc[0:1000,7]

#Lets make them with caps:
for i in range(len(scont)):
	if scont[i] == "controversial":
		scont[i] = "Controversial"
	if scont[i] == "somewhat controversial":
		scont[i] = "Somewhat Controversial"
	if scont[i] == "not controversial":
		scont[i] = "Not Controversial"
	if scont[i] == "unknown":
		scont[i] = "unk"


#columns the paper says were used for the summaries:

fa_fe = [i.lower() for i in list(fa)]
fa_ch = ["power","negemo","anger","tone","drives","percept","comma","see","discrep",\
		 "auxverb","dic","allpunc","risk","otherp","anx","function","pronoun","ppron",\
		  "cogproc","number","clout","negate","social","leisure","we","analytic",\
		  "differ","affect","achieve","certain","sad","tentat","work","prep","wc",\
		  "reward","wps","space","article","verb","hear","period","affiliation","relativ"]

ind2 = []
for i in fa_ch:
	for j in range(len(fa_fe)):
		if i == fa_fe[j]:
			ind2 += [j]

fach_su = fa.iloc[:,ind2]

#Note we are missing standard devation and entropy.
#Lets include them: (this might be wrong.)

sc = su.iloc[0:1000,3]
ssc = su.iloc[0:1000,4]
snc = su.iloc[0:1000,5]

#for stand dev
ssd = []
mean = 20/3
for i in range(len(sc)):
	ssd += [sqrt(sc[i]*(sc[i]-mean)**2+ssc[i]*(ssc[i]-mean)**2+snc[i]*(snc[i]-mean)**2)]

ssd = [i/sqrt(20) for i in ssd]

#for entropy
sen = []
for i in range(len(sc)):
	if sc[i] == 0: sc[i] = 1
	if ssc[i] == 0: ssc[i] = 1
	if snc[i] == 0: snc[i] = 1

	sen += [20*log(20)-(sc[i]*log(sc[i])+ssc[i]*log(ssc[i])+snc[i]*log(snc[i]))]

sen = [i/20 for i in sen]

summaries_disp = pd.DataFrame(data={"Entropy":sen})
summaries = fach_su
summaries_r = scont
#There we go. Summaries are the factors, summaries_r is responses.


#Before we remove the unknowns, lets complile the indeces of the agreed upon responses.

agreements_r = []
dis = []
for i in range(1000):
	if summaries_r.iloc[i] == titles_r.iloc[i] and summaries_r.iloc[i] != "unk":
		agreements_r += [summaries_r.iloc[i]]
	else:
		dis += [i]

agreements_r = pd.Series(agreements_r)
agreements = summaries.drop(dis)
agreements_ndm = fa_ndm.drop(dis)

#reindex

agreements.index = range(agreements.shape[0])
agreements_r.index = range(agreements.shape[0])
agreements_ndm.index = range(agreements.shape[0])

agreements_r.name = "Agreements"

agreements_r.to_pickle("agreements_r.pkl")
agreements.to_pickle("agreements.pkl")
agreements_ndm.to_pickle("agreements_ndm.pkl")

#We now remove the "unkowns" as we dont ahve any more data
#to break the ties. for the mains

unknns_s = []
unknns_t = []
for i in range(1000):
	if summaries_r[i] == "unk":
		unknns_s += [i]
	if titles_r[i] == "unk":
		unknns_t += [i]

summaries = summaries.drop(unknns_s)
summaries_r = summaries_r.drop(unknns_s)
summaries_ndm = fa_ndm.drop(unknns_s)

titles = titles.drop(unknns_t)
titles_r = titles_r.drop(unknns_t)
titles_ndm = fa_ndm.drop(unknns_t)


#reindex after the "drop" above.

summaries.index = range(summaries.shape[0])
summaries_r.index = range(summaries_r.shape[0])
summaries_ndm.index = range(summaries_r.shape[0])
titles.index = range(titles.shape[0])
titles_r.index = range(titles_r.shape[0])
titles_ndm.index = range(titles_r.shape[0])


#Lets name the reponses (this will be used later.)

summaries_r.name = "Summaries"
titles_r.name = "Titles"

# summaries.to_pickle("summaries_raw.pkl")
# summaries_r.to_pickle("summaries_r_raw.pkl")
# titles_r.to_pickle("titles_r_raw.pkl")
# titles.to_pickle("titles_raw.pkl")

#robust scaling causes every value (except NB) to increase, sometimes dramatically.
#The output as it comes out here is optimal, as far as I am concerned.
titles = pd.DataFrame(RobustScaler().fit_transform(titles),columns=list(titles))
summaries = pd.DataFrame(RobustScaler().fit_transform(summaries),columns=list(summaries))

#Lets pickle this for my other scripts.

summaries_disp.to_pickle("summaries_disp.pkl")
titles_disp.to_pickle("titles_disp.pkl")

summaries.to_pickle("summaries.pkl")
summaries_r.to_pickle("summaries_r.pkl")
summaries_ndm.to_pickle("summaries_ndm.pkl")
titles_r.to_pickle("titles_r.pkl")
titles.to_pickle("titles.pkl")
titles_ndm.to_pickle("titles_ndm.pkl")
'''