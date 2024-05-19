class MyUser{
private :
int id;
public:
int getId();
};

int MyUser::getId(){
    return this->id;
}

int main(char** argv, int argc){
    MyUser user1;
    MyUser* ptr1= new MyUser();
    return 0;
}