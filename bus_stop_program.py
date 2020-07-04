import sys
import getopt

args = sys.argv[1:]
opts, args = getopt.getopt(args, "r:g:b:h")

# Basic parameters

r_opt = [20]
g_opt = [6]
b_opt = [6]

for opt, arg in opts:
    if opt == "-r":
        x=int(arg)
        r_opt = [x]    
    elif opt == "-g":
        y=int(arg)
        g_opt == [y]
    elif opt == "-b":
        z=int(arg)
        b_opt = [z]
    elif opt == "-h":
        print("-r : Red bus line weight")
        print("-b : Blue bus line weight")
        print("-g : Green bus line weight")

import pandas as pd
import pydeck as pdk
import re

#bus stop location data
df_coord = pd.read_csv('bus_coord.csv',sep=",", encoding='cp949')
df_coord
lon = df_coord['X좌표']
lat = df_coord['Y좌표']

templist=[]
for i in range(len(lon)):    
    tempcoord=[lon[i],lat[i]]
    templist.append(tempcoord)

df_coord['coordinates'] = templist

#bustop number & The bus number
df_bus_line = pd.read_csv('bus_line.csv',sep=',', encoding='cp949')
df_bus_line.head()
df_bus_line_0 = df_bus_line[['노선번호','버스정류장ARS번호']]
df_bus_line_0.columns=['노선번호','정류소번호']

#merge
df_merge=pd.merge(left=df_bus_line_0, right = df_coord, how ="outer", on = '정류소번호')

#extract nan
df_merge=df_merge.dropna(subset=['X좌표'])
df_merge=df_merge.dropna(subset=['Y좌표'])
df_merge=df_merge.dropna(subset=['노선번호'])
df_merge=df_merge.dropna(subset=['정류소번호'])
df_merge=df_merge.dropna(subset=['coordinates'])

# line name data
df_bus_line_1 = df_bus_line_0[['노선번호']]
df_bus_line_2 = df_bus_line_1.drop_duplicates('노선번호')

line_num=[]
for i in range(len(df_bus_line_2)):
    line = df_bus_line_2.iloc[i,0]
    line_num.append(line)

df_geometry = pd.DataFrame(columns=['line_name'])
df_geometry['line_name'] = line_num

df_line = df_geometry.sort_values(by = ['line_name'])

#merge coordinate data in list
eachgroup = list(df_merge.groupby('노선번호'))
coordinate_dummy=[]
for i in range(len(eachgroup)):
    df_line_nums = eachgroup[i][1]
    df_line_num = df_line_nums.drop_duplicates(['정류소번호'],keep='first')
    series_coords = df_line_num['coordinates']
    arr_coords = series_coords.array
    list_coords = list(arr_coords)
    coordinate_dummy.append(list_coords)
    
def make_color(x): 
    X =re.findall("\d+",x)
    Y= float(X[0])
    Z = re.findall("N", x)
    z=""
    if 0<Y<10 and len(x)==2 : z = [255,255,0]
    elif Z==['N'] : z = [0,0,102]
    elif 0<Y<100 and len(x)>3 : z = [102,255,102]
    elif 100<=Y<1000 : z = [51,102,255]
    elif 1000<Y<9000: z = [51,204,51] 
    elif 9000<Y<10000: z = [255,0,51]  
    return z

def take_weight(x): 
    X =re.findall("\d+",x)
    Y = float(X[0])
    Z = re.findall("N", x)
    z=""
    if 0<Y<10 and len(x)==2 : z = [25]
    elif Z==['N'] : z = [10]
    elif 0<Y<100 and len(x)>3 : z = [25]
    elif 100<=Y<1000: z = b_opt
    elif 1000<Y<9000: z = g_opt 
    elif 9000<Y<10000: z = r_opt  
    return z

df_line['coordinates'] = coordinate_dummy
df_line['color'] = df_line['line_name'].apply(make_color)
df_line['weight'] = df_line['line_name'].apply(take_weight)

#Render

line_layer = pdk.Layer(
    'PathLayer',
    df_line,
    get_path='coordinates',
    get_width ='weight',
    get_color='[color[0],color[1],color[2]]',
)

point_layer = pdk.Layer(
    'ScatterplotLayer',
    df_merge,
    get_position = '[X좌표,Y좌표]',
    get_radius =20,
    get_fill_color = '[255,255,255]',
    pickable = True,
    auto_highlight=True
)


center = [126.9825876,37.5377887]
view_state = pdk.ViewState(longitude=center[0], latitude=center[1], zoom=10)

r = pdk.Deck(layers=[line_layer,point_layer],initial_view_state=view_state)
r.to_html("Bus_line_data_visulation.html")
