#version 120
attribute vec3 position;
attribute vec3 normal;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform float scale;
uniform float ambient_light;
uniform vec3 light_direction;
uniform vec4 light_color;
uniform vec4 model_color;
varying vec4 v_color;

void main(void)
{
   vec3 nn = normalize(normal);
   vec3 diffuseReflection = vec3(light_color) * vec3(model_color)
                             * max(ambient_light, dot(nn, light_direction));

   v_color = vec4(diffuseReflection , model_color[3]);
   gl_Position = projection * view * model * vec4(scale*position, 1.0);
}
