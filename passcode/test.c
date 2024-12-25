#include <stdio.h>

int main() {
    char regular_text[8] = "hello";
    char sensitive_text[8] = "private";
    
    printf("sensitive_text before: %s\n", sensitive_text);
    printf("Enter some text: ");
    scanf("%s", regular_text);  // Vulnerable: no length limit
    
    printf("\nAfter input:\n");
    printf("regular_text: %s\n", regular_text);
    printf("sensitive_text: %s\n", sensitive_text);
    
    return 0;
}