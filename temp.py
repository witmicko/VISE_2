img1 = self.img[307:928, 41:656]
center = (int(img1.shape[0] / 2) + 41, int(img1.shape[1] / 2) + 307)
ui.draw_degree_scale(dst, center, 41, 656)
lines = cv.detect_lines_p(img1)
if lines is not None:
    deg = []
    a, b, c = lines.shape
    for i in range(a):
        pt_a = (lines[i][0][0] + 41, lines[i][0][1] + 307)
        pt_b = (lines[i][0][2] + 41, lines[i][0][3] + 307)
        cv2.circle(dst, pt_a, 20, (0, 0, 255), 5)  # RED
        cv2.circle(dst, pt_b, 20, (0, 255, 0), 5)  # GREEN

        dist_a = np.math.hypot(pt_a[0] - center[0], pt_a[1] - center[1])
        dist_b = np.math.hypot(pt_b[0] - center[0], pt_b[1] - center[1])
        if dist_a < dist_b:
            degs = get_angle_between_points(center, pt_b)
        else:
            degs = get_angle_between_points(center, pt_a)

        deg.append(int(degs))
        if degs > 200:
            pass

        cv2.line(dst, pt_a, pt_b, (0, 0, 255), 3, cv2.LINE_AA)
        cv2.line(dst, pt_a, pt_b, (0, 0, 255), 3, cv2.LINE_AA)
    print(deg)




    {

    }