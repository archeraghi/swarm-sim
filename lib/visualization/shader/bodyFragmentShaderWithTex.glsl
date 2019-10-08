#version 120
uniform sampler2D texture;
varying vec3 v_diffuseReflection_colorless;
varying vec2 v_uv;
void main() {
    vec3 bla = v_diffuseReflection_colorless * vec3(texture2D(texture, v_uv).rgb);
    gl_FragColor = vec4(bla, 1);
}
