def bmi_calculater(weight,height):
    bmi=weight/((height/100)**2)
    return round (bmi,2)

def bmr_calculater(gender,age,weight,height):
    if gender == "Male":
        bmr=(10*weight)+(6.25*height)-(5*age)+5
        return bmr
    elif gender=="Female":
        bmr=(10*weight)+(6.25*height)-(5*age)-161
        return bmr
def tdee_calculater (bmr,activity):
    activity_factor= {"Sedentary":1.20,
                    "Lightly Active": 1.375,
                    "Moderately Active":1.55,
                    "very active":1.725,
                    "Extra Active":1.90}
    tdee=bmr*activity_factor[activity]
    return round(tdee,2)
def calories_target(tdee,aim):
    if aim == "weight maintain":
        calorie=tdee
    elif aim=="weight loss":
        calorie=tdee-400
    elif aim== "weight gain":
        calorie=tdee+300
    return round(calorie,2)


# print(bmi_calculater(60,150))
# bmr=bmr("male",25,50,150)
# print(bmr)
# tdee=tdee(bmr,"very active")
# print(tdee)
# print(calories_target(tdee,"weight gain"))

