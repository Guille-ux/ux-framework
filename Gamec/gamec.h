/* This program is free software: you can redistribute it and/or modify
/* it under the terms of the GNU General Public License as published by
/* the Free Software Foundation, either version 3 of the License, or
/* (at your option) any later version.
/* This program is distributed in the hope that it will be useful,
/* but WITHOUT ANY WARRANTY; without even the implied warranty of
/* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
/* GNU General Public License for more details.
/* You should have received a copy of the GNU General Public License
/* along with this program. If not, see <https://www.gnu.org/licenses/>.
/* Copyright (c) 2025 Guillermo Leira Temes
/* */

// By guille OpenGl display functions simplified

#include <GL/glut.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    float r;
    float g;
    float b;
} Color;

typedef struct {
    int w;
    int h;
    Color** data;
} Image;

typedef struct {
    float x;
    float y;
} Vertex;

typedef struct {
    Vertex a;
    Vertex b;
    Vertex c;
    Vertex d;
} Quad;

typedef struct {
   Vertex a;
   Vertex b;
   Vertex c;
} Tri;

#define RED    (Color){1.0, 0.0, 0.0}
#define GREEN  (Color){0.0, 1.0, 0.0}
#define BLUE   (Color){0.0, 0.0, 1.0}
#define YELLOW (Color){1.0, 1.0, 0.0}
#define PINK   (Color){1.0, 0.5, 0.5}
#define BROWN  (Color){0.6, 0.3, 0.1}
#define WHITE  (Color){1.0, 1.0, 1.0}
#define BLACK  (Color){0.0, 0.0, 0.0}

void minit(int argc, char** argv) {
    glutInit(&argc, argv);
}

void init(int width, int height, const char* name) {
    glutInitWindowSize(width != 0 ? width : 500, height != 0 ? height : 500);
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);
    glutCreateWindow(name);
    glClearColor(0.0, 0.0, 0.0, 1.0);
}

void clear() {
    glClear(GL_COLOR_BUFFER_BIT);
}
void redraw() {
    glutPostRedisplay();
}

void loop() {
    glutMainLoop();
}

void check() {
    glutMainLoopEvent();
}

Quad translatequad(Quad cube,  int movx, int movy) {
    cube.a.x = cube.a.x + movx;
    cube.a.y = cube.a.y + movy;
    cube.b.x = cube.b.x + movx;
    cube.b.y = cube.b.y + movy;
    cube.c.x = cube.c.x + movx;
    cube.c.y = cube.c.y + movy;
    cube.d.x = cube.d.x + movx;
    cube.d.y = cube.d.y + movy;
    return cube;
}

Vertex cordenates2D(Vertex v, int width, int height) {
    float m1 = v.x / (width / 2) - 1;
    float m2 = v.y / (height / 2) - 1;
    Vertex cordenates = {m1, m2};
    return cordenates;
}

void triangle(Color color, Vertex v1, Vertex v2, Vertex v3) {
    glColor3f(color.r, color.g, color.b);
    glBegin(GL_TRIANGLES);
    glVertex2f(v1.x, v1.y);
    glVertex2f(v2.x, v2.y);
    glVertex2f(v3.x, v3.y);
    glEnd();
    glFlush();
}

void rectangle(Color color, Vertex v1, Vertex v2, Vertex v3, Vertex v4) {
    glColor3f(color.r, color.g, color.b);
    glBegin(GL_QUADS);
    glVertex2f(v1.x, v1.y);
    glVertex2f(v2.x, v2.y);
    glVertex2f(v3.x, v3.y);
    glVertex2f(v4.x, v4.y);
    glEnd();
    glFlush();
}

void drawpixel(Color color, Vertex v1, int width, int height){
    glBegin(GL_POINTS);
    glColor3f(color.r, color.g, color.b); // Color rojo
    Vertex cor = cordenates2D(v1, width, height);
    glVertex2f(cor.x, cor.y);
    glEnd();
    glFlush();
}

int randint(int seed) {
    long int a = 23634824592;
    long int b = 810231804003;
    long int c = 93942331984420;

    int nseed = (a * seed + b) % c;
    return nseed;
}

Color rcolor(int numbera, int numberb, int numberc) {
    Color color = {numbera % 256, numberb % 256,numberc % 256};
    return color;
}

void rimage(int seeda, int seedb, int seedc, int w, int h) {
    for (int i = 0; i <= h; i++) {
        for (int o = 0; o <= w; o++) {
            Vertex v1 = {0 + o, 0 + i};
            drawpixel(rcolor(seeda, seedb, seedc), v1, w, h);
            seeda = randint(seeda);
            seedb = randint(seedb);
            seedc = randint(seedc);
            redraw();
            check();
    }
  }
}

Image ImageLoad(const char* archivo) {
    FILE* file = fopen(archivo, "rb");
    if (!file) {
        printf("Error al abrir el archivo.\n");
        exit(1);
    }

    // Leer el encabezado del archivo BMP
    unsigned char header[54];
    fread(header, sizeof(unsigned char), 54, file);

    // Extraer la anchura, altura y tamaño de la imagen del encabezado
    int width = *(int*)&header[18];
    int height = *(int*)&header[22];
    int size = height * width * 3;

    // Saltar al inicio de los datos de píxeles
    fseek(file, *(int*)&header[10], SEEK_SET);

    // Matriz para almacenar los datos de píxeles de la imagen
    Color** data = malloc(height * sizeof(Color*));
    if (!data) {
        printf("Error al asignar memoria para la matriz de colores.\n");
        exit(1);
    }

    // Leer los datos de píxeles y almacenarlos en la matriz
    unsigned char p[3];
    for (int h = 0; h < height; h++) {
        data[h] = malloc(width * sizeof(Color));
        if (!data[h]) {
            printf("Error al asignar memoria para la fila %d de la matriz de colores.\n", h);
            // Liberar memoria asignada previamente
            for (int i = 0; i < h; i++) {
                free(data[i]);
            }
            free(data);
            fclose(file);
            exit(1);
        }
        for (int w = 0; w < width; w++) {
            fread(p, sizeof(unsigned char), 3, file);
            data[h][w].r = p[2] / 255.0;
            data[h][w].g = p[1] / 255.0;
            data[h][w].b = p[0] / 255.0;
        }
    }

    // Cerrar el archivo y devolver la matriz de colores
    fclose(file);
    Image image = {width, height, data};
    return image;
}

int RenderImage(Image image, int w, int h, float x, float y) {
    for (int i = 0; i < image.h; i++) {
        for (int o = 0; o < image.w; o++) {
            Vertex v1 = {x + o, y + i};
            drawpixel(image.data[i][o], v1, w, h);
            redraw();
            check();
    }
  }
    return 0;
}

