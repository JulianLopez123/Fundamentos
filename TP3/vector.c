#include "vector.h"

vector_t *vector_crear(size_t tam) {
    if (tam == 0){
        return NULL;
    }
    vector_t *vector = malloc(sizeof(vector_t));
    if (vector == NULL){
        return NULL;
    }
    vector->valores=malloc(tam * sizeof(int));
    if (vector->valores == NULL){
        free(vector);
        return NULL;
    }
    vector->tam = tam;
    return vector;
}

void vector_destruir(vector_t* vector) {
    free(vector->valores);
    free(vector);
}

bool vector_guardar(vector_t *vector, size_t pos, int valor) {
    if(pos >= vector->tam){
        return false;
    }
    vector->valores[pos]=valor;
    return true;
}

bool vector_obtener(vector_t *vector, size_t pos, int *valor) {
    if(pos >= vector->tam){
        return false;
    }
    *valor = vector->valores[pos];
    return true;
}

size_t vector_largo(vector_t *vector) {
    return vector->tam;
}

void vector_por_escalar(vector_t *vector, int k) {
    for(size_t i=0; i < vector->tam ; i++)
        vector->valores[i] *= k;
}

vector_t* vector_sumar(vector_t *vector1, vector_t *vector2) {
    if(vector1->tam != vector2->tam){
        return NULL;
    }
    vector_t *vector3 = vector_crear(vector1->tam);
    if (vector3 == NULL){
        return NULL;
    }
    for(size_t i=0; i < vector3->tam ; i++){
        vector3->valores[i] = vector1->valores[i] + vector2->valores[i];
    }
    return vector3;
}

bool vector_redimensionar(vector_t *vector, size_t nuevo_tam) {
    if(nuevo_tam == 0){
        return false;
    }
    int *nuevo_valores = realloc(vector->valores, nuevo_tam * sizeof(int));
    if (nuevo_valores == NULL){
        return false;
    }
    vector->valores = nuevo_valores;
    vector->tam = nuevo_tam;
    return true;
}
