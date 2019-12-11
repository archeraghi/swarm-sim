// vertex shader for the OffsetColorCarryProgram

#version 150

// VBO 0 - per vertex
// vector of a face
attribute vec3 position;
// normal vector of the vector/face
attribute vec3 normal;

// VBO 1 - per instance - position offset of the model
attribute vec3 offset;
// VBO 2 - per instance - color of the model
attribute vec4 color;
// VBO 3 - per instance - is carried
attribute float carried;


// uniforms
// projection matrix
uniform mat4 projection;
// view matrix
uniform mat4 view;
// world matrix
uniform mat4 world;
// scaling of the position
uniform vec3 world_scaling;
// scaling of the size
uniform vec3 model_scaling;
// min value of brightness
uniform float ambient_light;
// direction of the parallel lightsource
uniform vec3 light_direction;
// color of the parallel lightsource
uniform vec4 light_color;

// varying color for fragment shader
varying vec4 v_color;


void main(void)
{
    vec3 nn = normalize(normal);
    vec3 diffuseReflection = vec3(light_color) * vec3(color)
                             * max(max(ambient_light, dot(nn, light_direction)), dot(-nn, light_direction));

    mat4 use_world = world;
    use_world[3] += vec4(offset * world_scaling, 0);
    float alpha = color[3];
    if(carried > 0.5){
        use_world[0][0] = 0.5;
        use_world[1][1] = 0.5;
        use_world[2][2] = 0.5;
        use_world[3][0] += 0.2;
        use_world[3][1] += 0.2;
        use_world[3][2] += 0.2;
        alpha = 0.8;
    }

    v_color = vec4(diffuseReflection, alpha);

    gl_Position = projection  * view * use_world * vec4(position * model_scaling, 1.0);
}

