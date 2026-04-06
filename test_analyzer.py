import sys, os
sys.path.insert(0, os.path.abspath('backend'))
sys.path.insert(0, os.path.abspath('compiler'))
sys.path.insert(0, os.path.abspath('.'))

from compiler.analyzer import analyze
import traceback

codes = [
    'int main() { char *buf = malloc(10); free(buf); printf(buf); }',
    'int main() { FILE *f = fopen("1.txt", "r"); if(f==NULL) return 0; }',
    'int main() { char buf[100]; strcpy(buf, "abc"); }',
    'int main() { int *x; *x = 5; }',
    'int main() { int arr[10000]; printf("%s", arr); }',
    'void foo(int a) { if (a > 5) { printf("hi"); } else { return; } }',
    'int main() { for(int i=0; i<10; i++) { printf("hi"); } }',
    'int main() { while(1) { break; } }',
    'int main() { int a = 5; int b = 6; a = b; }',
    'int main() { char* p = malloc(10); p = NULL; }',
    'int main() { int *p = malloc(sizeof(int)); if (p == NULL) return 0; free(p); free(p); }',
    'int main() { int x = malloc(y * sizeof(int)); }',
    'int main() { FILE *tmp = tmpnam(NULL); }',
    'int main() { printf("Hello"); }'
]

for i, code in enumerate(codes):
    print(f"Testing {i}...")
    try:
        analyze(code)
    except Exception as e:
        print(f"Error on test {i}: {code}")
        traceback.print_exc()
