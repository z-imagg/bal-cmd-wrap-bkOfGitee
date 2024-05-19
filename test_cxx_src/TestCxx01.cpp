class MyUser{
private :
int id;
public:
MyUser(){

}
~MyUser(){
    
}
int getId();

};

int MyUser::getId(){
    return this->id;
}

int main(int argc, char** argv){
    MyUser user1;
    MyUser* ptr1= new MyUser();
    return 0;
}