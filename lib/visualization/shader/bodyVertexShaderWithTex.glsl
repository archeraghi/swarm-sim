#version 120
attribute vec3 position;
attribute vec3 normal;
attribute vec2 uv;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform float scale;
uniform float ambient_light;
uniform vec3 light_direction;
uniform vec4 light_color;
varying vec3 v_diffuseReflection_colorless;
varying vec2 v_uv;

void main(void)
{
   vec3 nn = normalize(normal);
   v_diffuseReflection_colorless = vec3(light_color) * max(ambient_light, dot(nn, light_direction));
   v_uv = uv;
   gl_Position = projection * view * model * vec4(scale*position, 1.0);
}
