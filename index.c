int strStr(char* haystack, char* needle) {
    int     i;
    int     k;
    int     index;

    i = 0;
    k = 0;
    index = -1;
    while (haystack[i])
    {
        if (needle[k] == haystack[i])
        {
            if (index == -1)
                index = i;
            k++;
        }
        if (needle[k] == '\0')
            return (index);
        i++;
    }
    return (-1);
}
