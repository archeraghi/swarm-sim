#version 300 es
layout (location = 4) in vec3 position;
uniform mat4 projection;
uniform mat4 view;
uniform vec4 model_color;
out vec4 v_color;
void main(void)
{
   v_color = model_color;
   gl_Position = projection * view * vec4(position, 1.0);
}
