#ifndef hashtable_h
#define hashtable_h

typedef struct {
  unsigned int size;
  unsigned int *keys;
  int *values;
} map;

map *createMap(int size);
void destroyMap(map *garbage);
int getItem(map *hashtable, unsigned int key);
int hasItem(map *hashtable, unsigned int key);
void addItem(map *hashtable, unsigned int key, int value);

#endif
