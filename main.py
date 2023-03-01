
#############################################
# Kural Tabanlı Sınıflandırma ile Potansiyel Müşteri Getirisi Hesaplama
#############################################

#############################################
# İş Problemi
#############################################
# Bir oyun şirketi müşterilerinin bazı özelliklerini kullanarak seviye tabanlı (level based) yeni müşteri tanımları (persona)
# oluşturmak ve bu yeni müşteri tanımlarına göre segmentler oluşturup bu segmentlere göre yeni gelebilecek müşterilerin şirkete
# ortalama ne kadar kazandırabileceğini tahmin etmek istemektedir.

# Örneğin: Türkiye’den IOS kullanıcısı olan 25 yaşındaki bir erkek kullanıcının ortalama ne kadar kazandırabileceği belirlenmek isteniyor.


#############################################
# Veri Seti Hikayesi
#############################################
# Persona.csv veri seti uluslararası bir oyun şirketinin sattığı ürünlerin fiyatlarını ve bu ürünleri satın alan kullanıcıların bazı
# demografik bilgilerini barındırmaktadır. Veri seti her satış işleminde oluşan kayıtlardan meydana gelmektedir. Bunun anlamı tablo
# tekilleştirilmemiştir. Diğer bir ifade ile belirli demografik özelliklere sahip bir kullanıcı birden fazla alışveriş yapmış olabilir.

# Price: Müşterinin harcama tutarı
# Source: Müşterinin bağlandığı cihaz türü
# Sex: Müşterinin cinsiyeti
# Country: Müşterinin ülkesi
# Age: Müşterinin yaşı

################# Uygulama Öncesi #####################

#    PRICE   SOURCE   SEX COUNTRY  AGE
# 0     39  android  male     bra   17
# 1     39  android  male     bra   17
# 2     49  android  male     bra   17
# 3     29  android  male     tur   17
# 4     49  android  male     tur   17

################# Uygulama Sonrası #####################

#       customers_level_based        PRICE SEGMENT
# 0   BRA_ANDROID_FEMALE_0_18  1139.800000       A
# 1  BRA_ANDROID_FEMALE_19_23  1070.600000       A
# 2  BRA_ANDROID_FEMALE_24_30   508.142857       A
# 3  BRA_ANDROID_FEMALE_31_40   233.166667       C
# 4  BRA_ANDROID_FEMALE_41_66   236.666667       C

import pandas as pd
pd.set_option("display.max_rows", None)
df = pd.read_csv("persona.csv")
#general informations in database
df.head()
df.shape
df.info()
#How many unique SOURCE are there?What are the frequency?
df["SOURCE"].nunique()
df["SOURCE"].value_counts()
#How many unique PRICEs are there?
df["PRICE"].nunique()
#How many sales were realized from which PRICE?
df["PRICE"].value_counts()
#How many sales were made in which country?
df["COUNTRY"].value_counts()
df.groupby("COUNTRY")["PRICE"].count()

df.pivot_table(values="PRICE",index="COUNTRY",aggfunc="count")
#How much was earned in total from sales by country?
df.groupby("COUNTRY")["PRICE"].sum()
df.groupby("COUNTRY").agg({"PRICE": "sum"})

df.pivot_table(values="PRICE",index="COUNTRY",aggfunc="sum")
#What are the sales numbers according to SOURCE types?
df["SOURCE"].value_counts()
#What are the PRICE averages by country?
df.groupby(by=['COUNTRY']).agg({"PRICE": "mean"})
#What are the PRICE averages by SOURCEs?
df.groupby(by=['SOURCE']).agg({"PRICE": "mean"})
#What are the PRICE averages in the COUNTRY-SOURCE breakdown?
df.groupby(by=["COUNTRY", 'SOURCE']).agg({"PRICE": "mean"})
#What are the average earnings in breakdown of COUNTRY, SOURCE, SEX, AGE?
df.groupby(["COUNTRY", 'SOURCE', "SEX", "AGE"]).agg({"PRICE": "mean"}).head()
#Sort the output by PRICE.
agg_df = df.groupby(by=["COUNTRY", 'SOURCE', "SEX", "AGE"]).agg({"PRICE": "mean"}).sort_values("PRICE", ascending=False)
agg_df.head()
#Convert the names in the index to variable names.
agg_df = agg_df.reset_index()
agg_df.head()
#Convert AGE variable to categorical variable and add it to agg_df.
bins = [0, 18, 23, 30, 40, agg_df["AGE"].max()]

mylabels = ['0_18', '19_23', '24_30', '31_40', '41_' + str(agg_df["AGE"].max())]

agg_df["age_cat"] = pd.cut(agg_df["AGE"], bins, labels=mylabels)
agg_df.head()
#Define new level based customers and add them as variables to the dataset.
agg_df['customers_level_based'] = agg_df[['COUNTRY', 'SOURCE', 'SEX', 'age_cat']].agg(lambda x: '_'.join(x).upper(), axis=1)
#
agg_df["customers_level_based"] = ['_'.join(i).upper() for i in agg_df.drop(["AGE", "PRICE"], axis=1).values]

agg_df.columns
#observation values
for row in agg_df.values:
    print(row)

[row[0].upper() + "_" + row[1].upper() + "_" + row[2].upper() + "_" + row[5].upper() for row in agg_df.values]

agg_df["customers_level_based"] = [row[0].upper() + "_" + row[1].upper() + "_" + row[2].upper() + "_" + row[5].upper() for row in agg_df.values]
agg_df.head()

agg_df = agg_df[["customers_level_based", "PRICE"]]
agg_df.head()

for i in agg_df["customers_level_based"].values:
    print(i.split("_"))

agg_df["customers_level_based"].value_counts()

agg_df = agg_df.groupby("customers_level_based").agg({"PRICE": "mean"})

agg_df = agg_df.reset_index()
agg_df.head()

agg_df["customers_level_based"].value_counts()
agg_df.head()
#Segment new customers (USA_ANDROID_MALE_0_18).
agg_df["SEGMENT"] = pd.qcut(agg_df["PRICE"], 4, labels=["D", "C", "B", "A"])
agg_df.head(30)
agg_df.groupby("SEGMENT").agg({"PRICE": "mean"})
#What segment does a 33-year-old Turkish woman using ANDROID belong to and how much income is expected to earn on average?
new_user = "TUR_ANDROID_FEMALE_31_40"
agg_df[agg_df["customers_level_based"] == new_user]
# In which segment and on average how much income would a 35 year old French woman using iOS expect to earn?
new_user = "FRA_IOS_FEMALE_31_40"
agg_df[agg_df["customers_level_based"] == new_user]
