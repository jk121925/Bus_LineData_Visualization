

## 1. Overview
- **Project Name : Seoul_BusStop_map**
- This project is for generating Seoul Bus stop map using pydeck. To get a quick intuition, see the images below .

## 2. Sample IMG
<img src = "https://raw.githubusercontent.com/jk121925/jk_coding_study/master/Sample%20image/sample_img.jpg"  width = "350"> 


## 3. Dependency
- **Python** : ver. 3.7.6
- **Pydeck** : ver. 0.3.0
- **pandas** : ver. 1.0.1

## 4. Usage  

- **Set MapboxAccessToken**
  ```
    To see the base map, you need a Mapbox access token. 
    Go (https://www.mapbox.com/) and make account.
    Add to environment variable like "MAPBOX_API_KEY = "your mapbox api token (start from pk...)"
  ```
- **Execute Program**  
  ```Bash
  > python bus_stop_program.py -r 10 -g 10 -b 10
  ```
- **Option Description**  
  ```Bash
  > python bus_stop_program.py -h
  -r : Red bus line weight
  -g : Green bus line weight
  -b : Blue bus line weight
  ```
  

## 5. Version
- Current up-to-date version : v1.0.0
