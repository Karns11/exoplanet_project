###########################################################
# 
#  CSE 231 project #5
#
#  Program to calculate if a given exoplanet can support life as we know it:
#  function to prompt user for a file to input
#  function to convert a string into a float, if not possible, return -1.
#  function to calculate density of a planet given mass and radius.
#  fuction to calculate if a planets temperature is within a habitable temp range.
#  funvtion to calculate the maxium distance in order to filter the data. 
#  a final function that includes the main body of code where we will
#  interact with the user.
#  close the file.
#  
#    
###########################################################


import math

#Constants
PI = math.pi   
EARTH_MASS =  5.972E+24    # kg
EARTH_RADIUS = 6.371E+6    # meters
SOLAR_RADIUS = 6.975E+8    # radius of star in meters
AU = 1.496E+11             # distance earth to sun in meters
PARSEC_LY = 3.262


def open_file():
    ''' function that takes in a string input and opens that file.
    parameters: none
    returns: the given file '''

    prompt = input("Input data to open: ")
    while True:
        try:
            return open(prompt+'.csv', 'r')
            break
        except FileNotFoundError:
            print("\nError: file not found.  Please try again.")
            prompt = input("Enter a file name: ")

def make_float(s):
    ''' Function that will take in a string and make it a float type
    s: string that will try to convert into a float
    returns: string in float format or -1 if not possible '''
    try:
        s_float = float(s)
    except ValueError:
        return -1
    return s_float
  
def get_density(mass, radius):
    ''' Function that will return the density based on the density of a given planets mass and radius
    mass: the given mass of a planet
    radius: the given radius of a planet
    returns: -1 if calculation isnt possible or the density of the planet '''
    if make_float(mass) <= 0 or make_float(radius) <= 0:
        return -1
    else:
        earth_terms_mass = float(mass) * EARTH_MASS
        earth_terms_radius = float(radius) * EARTH_RADIUS
        if earth_terms_radius == 0:
            return -1
        else:
            volume = ((4 * math.pi * earth_terms_radius**3) / 3)
            density = earth_terms_mass / volume
            return density


def temp_in_range(axis, star_temp, star_radius, albedo, low_bound, upp_bound):
    ''' Function that calculates the temperature of a planet and determines if it can support life
    axis: given axis of the planet
    star_temp: temperature of a planets star
    star_radius: radius of the planets star
    albedo: 0.5
    low_bound: 200.0
    upp_bound: 350.0
    returns; True if the planet can support life, False otherwise '''
    if make_float(axis) < 0 or make_float(star_temp) < 0 or make_float(albedo) < 0 or float(low_bound) < 0 or float(upp_bound) < 0:
        return False
    else:
        axis_au = float(axis) * float(AU)
        star_radius_meters = float(star_radius) * float(SOLAR_RADIUS)
        axis_au_2 = 2*axis_au
        planet_temp = (star_temp) * (((star_radius_meters)/(axis_au_2))**0.5) * (1-albedo)**0.25
        #planet_temp = ((star_temp) * ((star_radius_meters)**0.5) * (1-albedo)**0.25)/(2*axis_au)
        if float(low_bound) <= float(planet_temp) <= float(upp_bound):
            return True
        else:
            return False

def get_dist_range():
    ''' Function that prompts a user for a max distance in order to filter the data
    parameters: none
    returns: max distance  '''
    dist_prompt = input("\nEnter maximum distance from Earth (light years): ")
    while True:
        try:
            dist_prompt_float = float(dist_prompt)
            if dist_prompt_float > 0:
                break
            else:
                print("\nError: Distance needs to be greater than 0.")
                dist_prompt = input("\nEnter maximum distance from Earth (light years): ")
        except ValueError:
            print("\nError: Distance needs to be a float.")
            dist_prompt = input("\nEnter maximum distance from Earth (light years): ")
    return dist_prompt_float

def main():
    ''' main function to interact with user
    parameters: None
    returns: Nothing''' 
    print('''Welcome to program that finds nearby exoplanets '''\
          '''in circumstellar habitable zone.''')
    #initialize all counters/constant variables 
    the_file = open_file()
    grab_dist = get_dist_range()
    max_dist = float(grab_dist) / float(PARSEC_LY)
    low_bound = 200.00 #lower bound
    upp_bound = 350.00 #upper bound
    albedo = 0.5 #given albedo
    max_stars = -1 #max num of stars initial variable
    max_plans = -1 #max num of planets initial variable
    sum_mass = 0 #sum of mass intial variable
    valid_dist = 0 #valid distance initial variable
    num_plans_for_calc = 0 #variable used for avg mass calcualtion
    num_rocky = 0 #num of rocky planets initial variable
    num_gas = 0 #num of gas planets initial variable
    closest_rocky_dist = (10**8) * PARSEC_LY #variable used to find closest rocky distance
    rocky_dist = 0
    gas_dist = 0
    closest_gas_dist = (10**8) * PARSEC_LY #variable used to find closest gaseous distance
    num_habitable_planets = 0
    row_count = 0
    rocky_planet_name = '' #variable used to get the planets name
    gas_planet_name = '' #variable used to get the planets name
    #skip header line
    the_file.readline()
    #loop through each line
    for line in the_file:
        file_dist = line[114:]
        dist_float = make_float(file_dist) #convert the distance in the file to a float
        new_dist = (dist_float * float(PARSEC_LY)) #new distance to filter data on 
        if 0 < dist_float < max_dist: #if the distance of a planet is between 0 and max distance, then include that line
            #find the star radius column and make it a float
            file_star_radius = line[106:113]
            file_star_radius_float = make_float(file_star_radius)
            #find the star temp column and make it a float
            file_star_temp = line[97:105]
            file_star_temp_float = make_float(file_star_temp)
            #find the planet mass column and make it a float
            file_planet_mass = line[86:96]
            file_planet_mass_float = make_float(file_planet_mass)
            #find the planet radius column and make it a float
            file_planet_radius = line[78:85]
            file_planet_radius_float = make_float(file_planet_radius)
            #find the planet axis column and make it a float
            file_axis = line[66:77]
            file_axis_float = make_float(file_axis)
            #find the planets number column and make it an int
            file_num_plan = int(line[58:65])
            #find the number of stars column and make it an int
            file_num_stars = int(line[50:57])
            #find the planets name column and make it a str
            file_plan_name = str(line[:25]).strip()
            if file_num_stars > max_stars: #max stars calculation
                max_stars = file_num_stars
            if file_num_plan > max_plans: #max planets calculation
                max_plans = file_num_plan
            if file_planet_mass_float > 0.0: #This is my if statement for sum_mass calc
                sum_mass += file_planet_mass_float
                row_count += 1
            #else:
                #print(file_planet_mass_float) #Every mass is being inluded for the first test
            if file_star_radius_float >=0 and file_axis_float >=0 and file_planet_mass_float and make_float(new_dist) >=0 and file_star_temp_float >=0: #solves complex type issue 
                if temp_in_range(file_axis_float, file_star_temp_float, file_star_radius_float, albedo, float(low_bound), float(upp_bound)) == True: #determine if the planet is in habitable zone
                        num_habitable_planets += 1
                        if 0 < file_planet_mass_float < 10 or 0 < file_planet_radius_float < 1.5 or get_density(file_planet_mass_float, file_planet_radius_float) > 2000: #rocky determination
                                num_rocky += 1
                                #print(file_plan_name)
                                #rocky_planet_name = file_plan_name
                                if dist_float * PARSEC_LY < closest_rocky_dist: #closest rocky planet calculation
                                    closest_rocky_dist = dist_float * PARSEC_LY
                                    rocky_planet_name = file_plan_name
                        else: #gaseous determination
                            num_gas += 1
                            if dist_float * PARSEC_LY < closest_gas_dist: #closest gaseous planet calculation
                                closest_gas_dist = dist_float * PARSEC_LY
                                gas_planet_name = file_plan_name
    
    avg_mass = sum_mass / row_count #avg mass calculation outside of loop

    #all of my print statements
    print("\nNumber of stars in systems with the most stars: {:d}.".format(max_stars))
    print("Number of planets in systems with the most planets: {:d}.".format(max_plans))
    print("Average mass of the planets: {:.2f} Earth masses.".format(avg_mass))
    print("Number of planets in circumstellar habitable zone: {:d}.".format(num_habitable_planets))
    if num_gas ==0:
       print("No gaseous planet in circumstellar habitable zone.")
    if num_rocky ==0:
       print("No rocky planet in circumstellar habitable zone.")
    if num_rocky != 0:
        print("Closest rocky planet in the circumstellar habitable zone {} is {:.2f} light years away.".format(rocky_planet_name, closest_rocky_dist))
    if num_gas != 0:
        print("Closest gaseous planet in the circumstellar habitable zone {} is {:.2f} light years away.".format(gas_planet_name, closest_gas_dist))
    the_file.close() #close the file

if __name__ == "__main__":
    main()