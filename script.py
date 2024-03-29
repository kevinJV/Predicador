import numpy as np
import math
import matplotlib.pyplot as plt


del_t = 1
pos_x_og = 5
pos_y_og = 6
vel_x_og = 1 * del_t
vel_y_og = 0.5 * del_t

real_pos_noise_arr = []
real_vel_noise_arr = []
predicted_pos_noise_arr = []
#predicted_vel_noise_arr = []
predict_num = 4

ideal_positions = []

real_steps = []
real_positions = []
real_vel = []

#predicted_steps = []
predicted_positions = []
#predicted_vel = []
epochs = 40


func_matriz_a = [
    [1, 0, 1, 0],
    [0, 1, 0, 1],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
]


def w(sigma):
    return np.random.normal(0, sigma)

def predicted_step(pos_x, pos_y, vel_x, vel_y, sig_v, sig_p, observer_coor, iterator):
    w_pos_x = w(sig_p*1.2)
    w_pos_y = w(sig_p*1.2)
    w_vel_x = w(sig_v*1.2)
    w_vel_y = w(sig_v*1.2)

    #print(iterator, "#########")
    #r = np.sqrt((observer_coor[0]-pos_x)**2+(observer_coor[1]-pos_y)**2)
    #print("R", ": ", r)
    # theta = np.arctan((observer_coor[0]-pos_x)/(observer_coor[1]-pos_y))
    #theta = math.atan((observer_coor[0]-pos_x)/(observer_coor[1]-pos_y))
    #print("arch: ", (observer_coor[0]-pos_x)/(observer_coor[1]-pos_y))
    #print("Theta: ", math.degrees(theta))
    #print(observer_coor[0], "-", pos_x, "/", observer_coor[1], "-", pos_y)
    
    #print("cos", r * math.cos(theta))
    #print("sin", r * math.sin(theta))
    #print("#########")

    step_arr = np.array([pos_x, pos_y, vel_x, vel_y])
    vel_arr = np.array([vel_x, vel_y, 0, 0])
    w_arr = np.array([w_pos_x, w_pos_y, w_vel_x, w_vel_y])
    arr = np.add(np.add(step_arr, vel_arr), w_arr)    

    print(iterator)
    predicted_pos_noise_arr[iterator].append([w_pos_x, w_pos_y])
    #predicted_vel_noise_arr[iterator].append([w_vel_x, w_vel_y])
    #predicted_steps[iterator].append([w_pos_x, w_pos_y])
    #predicted_vel[iterator].append([w_vel_x, w_vel_y])
    predicted_positions[iterator].append([arr[0], arr[1]])

    return arr[0], arr[1], arr[2], arr[3]

def real_step(pos_x, pos_y, vel_x, vel_y, sig_v, sig_p):
    w_pos_x = w(sig_p)
    w_pos_y = w(sig_p)
    w_vel_x = w(sig_v)
    w_vel_y = w(sig_v)

    step_arr = np.array([pos_x, pos_y, vel_x, vel_y])
    vel_arr = np.array([vel_x, vel_y, 0, 0])
    w_arr = np.array([w_pos_x, w_pos_y, w_vel_x, w_vel_y])
    arr = np.add(np.add(step_arr, vel_arr), w_arr)

    real_pos_noise_arr.append([w_pos_x, w_pos_y])
    real_vel_noise_arr.append([w_vel_x, w_vel_y])
    real_steps.append([w_pos_x, w_pos_y])
    real_vel.append([w_vel_x, w_vel_y])
    real_positions.append([arr[0], arr[1]])

    return arr[0], arr[1], arr[2], arr[3]


def ideal_step(pos_x, pos_y, vel_x, vel_y):

    step_arr = np.array([pos_x, pos_y, vel_x, vel_y])
    vel_arr = np.array([vel_x, vel_y, 0, 0])

    arr = np.add(step_arr, vel_arr)

    ideal_positions.append([arr[0], arr[1]])
    return arr[0], arr[1], arr[2], arr[3]


def get_vector(array, pos):
    vector = []
    for i in array:
        vector.append(i[pos])
    return vector


if __name__ == "__main__":
    sig_v = 0.01
    sig_p = 0.4

    # Ideal
    pos_x = pos_x_og
    pos_y = pos_y_og
    vel_x = vel_x_og
    vel_y = vel_y_og
    for i in range(0, epochs):
        pos_x, pos_y, vel_x, vel_y = ideal_step(pos_x, pos_y, vel_x, vel_y)
    print("Ideal positions ", np.array(ideal_positions))

    # Real
    pos_x = pos_x_og
    pos_y = pos_y_og
    vel_x = vel_x_og
    vel_y = vel_y_og
    for i in range(0, epochs):
        pos_x, pos_y, vel_x, vel_y = real_step(
            pos_x, pos_y, vel_x, vel_y, sig_v, sig_p)
    print("Real positions ", np.array(real_positions))    
    print("Real pos noises: ", np.array(real_pos_noise_arr))
    print("Real vel noises: ", np.array(real_vel_noise_arr))
    print("Real steps ", np.array(real_steps))
    print("Real vel ", np.array(real_vel))

    # Predicciones
    for k in range(0, predict_num):
        pos_x = pos_x_og
        pos_y = pos_y_og
        vel_x = vel_x_og
        vel_y = vel_y_og
        r = 0
        theta = 0        
        # Observador
        observer_coor = [10, 10]
        predicted_pos_noise_arr.append([])
        #predicted_vel_noise_arr.append([])
        #predicted_steps.append([])
        #predicted_vel.append([])
        predicted_positions.append([])
        for i in range(0, epochs):
            pos_x, pos_y, vel_x, vel_y = predicted_step(pos_x, pos_y, vel_x, vel_y, sig_v, sig_p, observer_coor, k)
    print("Predicted positions ", np.array(predicted_positions))    
    print("Predicted pos noises: ", np.array(predicted_pos_noise_arr))
    #print("Predicted vel noises: ", np.array(predicted_vel_noise_arr))
    #print("Predicted steps ", np.array(predicted_steps))
    #print("Predicted vel ", np.array(predicted_vel))

    plt.title('Gráficas')
    plt.xlabel("x")
    plt.ylabel("y")
    colors = ['b', 'g', 'r', 'c', 'm']

    # Ideal
    x = get_vector(ideal_positions, 0)    
    y = get_vector(ideal_positions, 1)        
    plt.plot(x, y, color='k', lw=2)

    # Predicado
    color_num = 0
    print(len(predicted_positions))
    for predicado in predicted_positions:
        x = get_vector(predicado, 0)    
        y = get_vector(predicado, 1)        
        plt.plot(x, y, color=colors[color_num % len(colors)], lw=1)
        color_num += 1

    # Real
    x = get_vector(real_positions, 0)
    y = get_vector(real_positions, 1)    
    plt.plot(x, y, color='y', lw=3)

    # P = F * P * Ft + Q
    f = np.array(func_matriz_a)
    q = [
        [sig_p,0,0,0],
        [0,sig_p,0,0],
        [0,0,sig_v,0],
        [0,0,0,sig_v]
    ]
    p = q

    print("Esta es f\n", f)
    print("Esta es p\n", p)
    print("Esta es f transposed\n", f.transpose())
    print("Esta es q\n", q)
    p = f * p * f.transpose() + q
    print("Esta es p\n", p)

    p = np.add(np.dot(np.dot(f, p), f.transpose()), q)
    print("Esta es p\n", p)

    # P = F * P * Ft + Q

    r = np.array([
        [sig_p*1.2, 0],
        [0, sig_p*1.2]
    ])

    h = np.array([
        [1,0,0,0],
        [0,1,0,0]
    ])

    temp = np.dot(p, h.transpose())

    # for i in range(0, epochs):

    k = np.dot(temp, np.linalg.inv(np.add(np.dot(np.dot(h, p),h.transpose()), r)))
    print("Esta es k\n", k)

    # X = F * X + w
    
    # Z = H * X + u


    plt.show()
