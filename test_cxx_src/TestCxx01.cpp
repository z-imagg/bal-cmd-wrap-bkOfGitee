class MyUser{
private :
int id;
public:
int getId();
};

int MyUser::getId(){
    return this->id;
}