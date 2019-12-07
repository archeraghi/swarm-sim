#version 330
precision mediump float;
in vec4 v_color;
in vec4 gl_FragCoord;
out vec4 FragColor;
void main() {
    FragColor = v_color;
    // FragColor = vec4(vec3(gl_FragCoord.z), v_color[3]);
}
