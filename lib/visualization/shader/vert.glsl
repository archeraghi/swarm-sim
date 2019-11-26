#version 300 es
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 normal;
layout (location = 2) in vec3 offset;
layout (location = 3) in vec3 color;
uniform mat4 projection;
uniform mat4 view;
uniform float scale;
uniform float ambient_light;
uniform vec3 light_direction;
uniform vec4 light_color;
uniform vec4 model_color;
out vec4 v_color;
void main(void)
{
   vec3 nn = normalize(normal);
   vec3 diffuseReflection = vec3(light_color) * vec3(model_color)
                             * max(max(ambient_light, dot(nn, light_direction)), dot(-nn, light_direction));

   mat4 model = mat4(1,0,0,0,
                     0,1,0,0,
                     0,0,1,0,
                     offset,1);
   v_color = vec4(diffuseReflection , model_color[3]);
   gl_Position = projection * view * model * vec4(scale*position, 1.0);
}
