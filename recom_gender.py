from pulp import *
import re
import math

#a simple distribution solver with man:50% female:50%
def simple_distribution_solver(total_participant=220, distribution_percentage={'male': 0.5, 'female': 0.5}):
    gender_dict = {}

    #set up
    prob = LpProblem("Simple solver", LpMaximize)

    # Create problem variables with 50% male 50% female distribution for 220 people
    # x1 = LpVariable("male", 0, None, LpInteger)
    # x2 = LpVariable("female", 0, None, LpInteger)
    x = []
    for item in distribution_percentage.keys():
        x.append([LpVariable(item, 0, None, LpInteger), distribution_percentage[item]])

    # set up problem
    #prob += x1+x2, total_participant
    firstTime = True
    for lp_var in x:
        if firstTime:
            all_x = lp_var[0]
            firstTime = False
        else:
            all_x = all_x + lp_var[0]

    prob += all_x, total_participant

    # Constraints
    # prob += (x1*1/total_participant) == .5
    # prob += (x2*1/total_participant) == .5
    for lp_var in x:
        prob += (lp_var[0]*1/total_participant) == (lp_var[1])

    prob+= all_x == total_participant


    prob
    prob.solve()
    #pulp.LpStatus[prob.status]     #If you want to print status

    for v in prob.variables():
        gender_dict[v.name]=math.ceil(v.varValue)

    return gender_dict



#already have paticipants waiting for future pairs
def have_sample(total_participant=220,num_exist=100,participant_exists={'male':60,'female':40},
                pair_distribution={'male':0.5,'female':0.5}):
    #prob 2:
    gender_dict = {}
    #set up
    prob = LpProblem("solver", LpMaximize)
    # Create problem variables
    # x1=LpVariable("male",0,None,LpInteger)
    # x2=LpVariable("female",0, None, LpInteger)
    x =[]
    for k in pair_distribution.keys():
        x.append([LpVariable(k,0,None,LpInteger),pair_distribution[k]])

    first_time = True
    for lp_var in x:
        if first_time:
            all_x = lp_var[0]
            first_time = False
        else:
            all_x = all_x + lp_var[0]

    sub_total = total_participant-num_exist
    prob += all_x, sub_total

    for lp_var in x:
        prob += (lp_var[0]+participant_exists[str(lp_var[0])])/total_participant == pair_distribution[str(lp_var[0])]

    # x3 = exist_male
    # x4 = exist_female
    # set up problem
    # prob += x1+x2,total
    # Constraints
    # prob += x1+x3+x2+x4 == total
    # prob += ((x1+x3)/total) == .50
    # prob += ((x1+x3)/total) >= .48
    # prob += ((x2+x4)/total) == .50
    # prob += ((x2+x4)/total) >= .48
    # prob += x3+x4 == exist

    prob
    prob.solve()

    for v in prob.variables():
        if v.varValue != None:
            gender_dict[v.name] = v.varValue

    return gender_dict

#pair distribution
def pair_distribution(total_participants=220, exist_participants=100,exist_pair_dist={'MM':52,'MF':8,'FM':8,'FF':32},pair_dist={'MM':.25,'FM':.25,'MF':.25,'FF':.25}):

    pair_dict={}
    # linear problem set up
    prob = LpProblem("Simple solver", LpMaximize)

    x =[]
    for key in pair_dist.keys():
        x.append([LpVariable(key,0,None,LpInteger),pair_dist[key]])

    sub_total = total_participants-exist_participants

    first_time = True
    for lp_var in x:
        if first_time:
            all_x = lp_var[0]
            first_time = False
        else:
            all_x = all_x + lp_var[0]
    #linear prob
    prob += all_x, sub_total
    #prob3 += x5+x6,total

    #constraints
    prob += all_x == sub_total
    for lp_var in x:
        prob += (lp_var[0]+exist_pair_dist[str(lp_var[0])])/total_participants <= (pair_dist[str(lp_var[0])]+.02)
        prob += (lp_var[0]+exist_pair_dist[str(lp_var[0])])/total_participants >= (pair_dist[str(lp_var[0])]-.02)

    # prob3 += x1+x2+x3+x4 == sub_total
    # prob3 += (x1+(pre_male-pre_MF))/total <= .25
    # prob3 += (x1+(pre_male-pre_MF))/total >= .23
    # prob3 += (x2+pre_MF)/total <= .27
    # prob3 += (x2+pre_MF)/total >= .23
    # prob3 += (x3+pre_FM)/total <= .27
    # prob3 += (x3+pre_FM)/total >= .23
    # prob3 += (x4+(pre_female-pre_FM))/total <= .27
    # prob3 += (x4+(pre_female-pre_FM))/total >= .23
    # prob3 += (x5+pre_male)/total == .5
    # prob3 += (x6+pre_female)/total == .5

    prob
    prob.solve()
    pulp.LpStatus[prob.status]

    for v in prob.variables():
        pair_dict[v.name] = v.varValue

    return pair_dict
#gender_age_dist
def age(total_participant=220,participant_exist=100, num_age={'19_24':43,'25_34':24,'35_45':33}
        ,age_dist={'19_24':.33,'25_34':.33,'35_45':.33}):

    r_age_dict ={}

    prob = LpProblem("solver", LpMaximize)
    # Create problem variables
    x =[]
    for k in age_dist.keys():
        x.append([LpVariable(k,0,None,LpInteger),age_dist[k]])

    first_time = True
    for lp_var in x:
        if first_time:
            all_x = lp_var[0]
            first_time = False
        else:
            all_x = all_x + lp_var[0]

    sub_total = total_participant - participant_exist
    prob += all_x , sub_total

    # prob += x1+x2+x3,120
    prob += all_x == sub_total
    #Constraints
    for lp_var in x:
        prob += (lp_var[0]+num_age[str(lp_var[0])])/total == age_dist[str(lp_var[0])]

    # prob += (x1+age_dict['19-24'])/total == .33
    # #prob += (x1+age_dict['19-24'])/total >= .31
    # prob += (x2+age_dict['25-34'])/total == .33
    # #prob += (x2+age_dict['25-34'])/total >= .31
    # prob += (x3+age_dict['35-45'])/total == .33
    # #prob += (x3+age_dict['25-34'])/total >= .31
    # prob += x1+x2+x3 == 120

    prob
    prob.solve()
    pulp.LpStatus[prob.status]

    for v in prob.variables():
        r_age_dict[v.name] = math.ceil(v.varValue)

    return r_age_dict

def gender_age(num_gender,age_str,sample,gender_age_dist={'male':.5,'female':.5}):

    gender_age ={}

    prob = LpProblem("solver", LpMaximize)
    # Create problem variables
    x =[]

    for k in gender_age_dist.keys():
        x.append([LpVariable(k,0,None,LpInteger),gender_age_dist[k]])

    first_time = True
    for lp_var in x:
        if first_time:
            all_x = lp_var[0]
            first_time = False
        else:
            all_x = all_x + lp_var[0]

    #prob += x1+x2, total
    prob += all_x, num_gender
    #constraints
    for lp_var in x:
        if str(lp_var[0]) == 'male':
            prob += (lp_var[0]+sample[0])/num_gender <= gender_age_dist[str(lp_var[0])]+.02
            prob += (lp_var[0]+sample[0])/num_gender >= gender_age_dist[str(lp_var[0])]-.02
        else:
            prob += (lp_var[0]+sample[1])/num_gender <= gender_age_dist[str(lp_var[0])]+.02
            prob += (lp_var[0]+sample[1])/num_gender >= gender_age_dist[str(lp_var[0])]-.02

    # prob += (x1+sample_dict[k][0])/73 <= .52
    # prob += (x1+sample_dict[k][0])/73 >= .48
    # prob += (x2+sample_dict[k][1])/73 <= .52
    # prob += (x2+sample_dict[k][1])/73 >= .48

    #prob += x1+x2 == total


    prob.solve()
    pulp.LpStatus[prob.status]

    for v in prob.variables():
        gender_age[v.name] = math.ceil(v.varValue)


    return gender_age,age_str


if __name__ == "__main__":

    #testing 110 exists with 60% male 50% female
    total = 220
    exist = 100

    print(simple_distribution_solver())

    print(have_sample(float(total),float(exist),{'male':60,'female':40}))


    #gender and age

    tmp_list=[]
    #age distribution needed for each age
    age_dict={'19_24':73,'25_34':73,'35_45':74}
    sample_dict = {'19_24':[26,17],'25_34':[17,7],'35_45':[17,16]}
    # r_age_dict = age(float(total),age_dict)
    #print(r_age_dict)
    for k,v in age_dict.items():
        tmp_list.append(gender_age(v,k,sample_dict[k],{'male':0.5,'female':0.5}))


    #tidy data recevied
    age_list=[]
    male_list =[]
    female_list = []
    gender_age = {'age_legend':age_list,'male':male_list,'female':female_list}
    # print(tmp_list)
    for e in tmp_list:
        gender_age['age_legend'].append(e[1])
        for k, v in e[0].items():
            if k =="male":
                gender_age['male'].append(v)
            else:
                gender_age['female'].append(v)

    print(gender_age)

    #pair distribution
    #Already have 100 people MM:52,MF:8,FM:8,FF:32
    print(pair_distribution(total,100,{'MM':52,'MF':8,'FM':8,'FF':32},{'MM':.25,'FM':.25,'MF':.25,'FF':.25}))
    #gender pair within age
    age_gender_pair={}
    for k, v in age_dict.items():
        age_gender_pair[k]=pair_distribution(v,0,{'MM':0,'MF':0,'FM':0,'FF':0},{'MM':.25,'FM':.25,'MF':.25,'FF':.25})
    print(age_gender_pair)
