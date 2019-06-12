import numpy as np
import matplotlib.pyplot as plt

del_t = 1
pos_x_og = 5
pos_y_og = 6
vel_x_og = 1 * del_t
vel_y_og = 0.5 * del_t

noise_arr = []
predict_num = 4

ideal_positions = []

steps = []
positions = []

predicted_steps = []
predicted_positions = []
epochs = 40


func_matriz_a = [
    [1, 0, 1, 0],
    [0, 1, 0, 1],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
]


def w(sigma):
    return np.random.normal(0, sigma)


def step(pos_x, pos_y, vel_x, vel_y, sig_v, sig_p):
    w_pos_x = w(sig_p)
    w_pos_y = w(sig_p)
    w_vel_x = w(sig_v)
    w_vel_y = w(sig_v)

    step_arr = np.array([pos_x, pos_y, vel_x, vel_y])
    vel_arr = np.array([vel_x, vel_y, 0, 0])
    w_arr = np.array([w_pos_x, w_pos_y, w_vel_x, w_vel_y])
    arr = np.add(np.add(step_arr, vel_arr), w_arr)

    noise_arr.append([w_pos_x, w_pos_y, w_vel_x, w_vel_y])
    steps.append(np.array(arr).tolist())
    positions.append([arr[0], arr[1]])

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
    print("ideal positions ", np.array(ideal_positions))

    # Real
    pos_x = pos_x_og
    pos_y = pos_y_og
    vel_x = vel_x_og
    vel_y = vel_y_og
    for i in range(0, epochs):
        pos_x, pos_y, vel_x, vel_y = step(
            pos_x, pos_y, vel_x, vel_y, sig_v, sig_p)
    print("a ", np.array(noise_arr))
    print("steps ", np.array(steps))
    print("positions ", np.array(positions))

    # # Predicciones
    # for k in range(0, predict_num):
    #     pos_x = pos_x_og
    #     pos_y = pos_y_og
    #     vel_x = vel_x_og
    #     vel_y = vel_y_og
    #     for i in range(0, epochs):
    #         pos_x, pos_y, vel_x, vel_y = step(
    #             pos_x, pos_y, vel_x, vel_y, sig_v, sig_p)
    #     # print("a ", np.array(noise_arr))
    #     # print("steps ", np.array(steps))
    #     # print("positions ", np.array(positions))

    plt.title('Gráficas')
    plt.xlabel("x")
    plt.ylabel("y")
    colors = ['b', 'g', 'r', 'c', 'm']

    x = get_vector(ideal_positions, 0)
    print(x)
    y = get_vector(ideal_positions, 1)    
    print(y)
    plt.plot(x, y, color='k', lw=2)

    x = get_vector(positions, 0)
    print("x: ")
    print(x)
    y = get_vector(positions, 1)    
    print("y: ")
    print(y[1], ", ",x[1])
    plt.plot(x, y, color='y', lw=3)
    plt.show()
