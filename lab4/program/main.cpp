#include <string>
#include <iostream>
#include <fstream>
#include <thread>
#include <vector>
#include <locale.h>
#include <mutex>
#include <windows.h>

#define M_STR 1024
#define dic_len 100000
#define thread_count 1

struct args{
    args(int &result0,int &res_string0,int data_start0,int data_end0,std::vector <std::string> &data0,std::string &serch_str0,std::mutex &mtx0):
        result(result0),
        res_string(res_string0),
        data_start(data_start0),
        data_end(data_end0),
        data(data0),
        serch_str(serch_str0),
        mtx(mtx0)
    {};
    int &result;
    int &res_string;
    int data_start;
    int data_end;
    std::vector <std::string> &data;
    std::string &serch_str;
    std::mutex &mtx;
};

double PCFreq = 0.0;
__int64 CounterStart = 0;

void StartCounter()
{
    LARGE_INTEGER li;
    if(!QueryPerformanceFrequency(&li))
    std::cout << "QueryPerformanceFrequency failed!\n";

    PCFreq = double(li.QuadPart);///1000.0;

    QueryPerformanceCounter(&li);
    CounterStart = li.QuadPart;
}

double GetCounter()
{
    LARGE_INTEGER li;
    QueryPerformanceCounter(&li);
    return double(li.QuadPart-CounterStart)/PCFreq;
}

int min(int i1, int i2)
{
    return (i1 < i2) ? i1 : i2;
}

int min(int i1, int i2, int i3)
{
    i2 = (i2 < i3) ? i2 : i3;
    return (i1 < i2) ? i1 : i2;
};

int min(int i1, int i2, int i3, int i4)
{
    i3 = (i3 < i4) ? i3 : i4;
    i2 = (i2 < i3) ? i2 : i3;
    return (i1 < i2) ? i1 : i2;
};

int max(int i1, int i2)
{
    return (i1 > i2) ? i1 : i2;
}

int string_count(std::string &name)
{
    int i = 0;
   std::ifstream f(name);
   while (!(f.eof() or f.fail()))
   {
       if (f.get() == '\n')
           i++;
   }
    return i;
}

int DemLevAlg(std::string &str1, std::string &str2)
{
    int f;
    int l, l1, l2;

    //if (str01.length() > str02.length())
    //{
     //  std::string &str1 = str02;
     //  std::string &str2 = str01;
    //}

    //std::cout << str1 << ' ' << str2;
    int n = str1.length() + 1, m = str2.length() + 1;

    int matrix[n + 1][3];
    for (int i = 0; i < n; i++)
        matrix[i][0] = i;

    for (int j = 1; j < m; j++)
    {
        l = j % 3;
        l1 = (l + 2) % 3;
        l2 = (l + 1) % 3;
        matrix[0][l] = j;
        for (int i = 1; i < n; i++)
        {
            if (str1[i - 1] == str2[j - 1])
                f = 0;
            else
                f = 1;
            if (i != 1 and j != 1 and str1[i - 1] == str1[j-2] and str2[j- 1] == str1[i-2])
                matrix[i][l] = min(matrix[i-2][l2] + 1, matrix[i-1][l1] + f, matrix[i-1][l] + 1, matrix[i][l1] + 1);
            else
                matrix[i][l] = min(matrix[i-1][l1] + f, matrix[i-1][l] + 1, matrix[i][l1] + 1);
            //std::cout << matrix[i][l] << ' ';
        }
        //std::cout << '\n';
    }
    return matrix[n - 1][(m - 1)%3];
}

void thread_work(args arg)
{
    int temp_res = DemLevAlg(arg.data.at(arg.data_start), arg.serch_str), temp_str = arg.data_start;
    int tmp;
    for (int i = arg.data_start; i < arg.data_end; i++)
    {
        tmp = DemLevAlg(arg.data.at(i), arg.serch_str);
        if (tmp < temp_res)
        {
            temp_res = tmp;
            temp_str = i;
        }
    }
    arg.mtx.lock();
        if (arg.result > temp_res)
        {
            arg.result = temp_res;
            arg.res_string = temp_str;
        }
    arg.mtx.unlock();
};

void run_theared(int th_count, int &res_str, int &res_int, int all_data, std::vector <std::string> &data, std::string &search)
{
    std::thread thr[th_count];
    int ud_data = all_data / th_count;
    std::mutex mtx;
    for (int i = 0; i < th_count - 1; i++)
    {
        args arg(res_int, res_str, i * ud_data, ud_data * (i + 1), data, search, mtx);
        thr[i] = std::thread(thread_work, arg);
    }
    args arg(res_int, res_str, (th_count - 1) * ud_data, all_data, data, search, mtx);
    thr[th_count - 1] = std::thread(thread_work, arg);
    for (int i = 0; i < th_count; i++)
        thr[i].join();

}

void LoadDictionary(std::vector <std::string> &dictionary, std::string &name)
{
   int n = min(string_count(name), dic_len);
   char str[M_STR];
   dictionary.resize(n);
   std::ifstream f(name);
   for (int i = 0; i < n; i++)
   {
       if (f.getline(str, M_STR, '\n'))
           dictionary.at(i) = str;
   }
}

int main(int argc, char *argv[])
{
    std::vector <std::string> dictionary;
    std::string file_name = "ENRUS.txt", serch_str;
    std::cout << "Input the word: ";
    serch_str = "searchstr";
    std::cin >> serch_str;
    LoadDictionary(dictionary, file_name);
    int res = serch_str.size(), res_str = 0, tmp = 0;
    for (int j = 100; j <= dictionary.size(); j*=10)
    {
        std::cout << "\n\nSize: " << j;
    StartCounter();
    for (int i = 0; i < j; i++)
    {
        tmp = DemLevAlg(dictionary.at(i), serch_str);
        //std::cout << tmp << '\n';
        if (tmp < res)
        {
            res = tmp;
            res_str = i;
        }
    }
    double time = GetCounter();
    std::cout << "\n\nThe closest word: " << dictionary[res_str];
    std::cout << "\n\nTime simple algoritm: " << time;
    for (int thc = 1; thc <= 16; thc*=2)
    {
        std::cout << "\n\nThreds: "<< thc;
        res = serch_str.size();
        StartCounter();
        run_theared(thc, res_str, res, j, dictionary, serch_str);
        time = GetCounter();
        std::cout << "\n\nThe closest word: " << dictionary[res_str];
        std::cout << "\n\nTime paralel algoritm: " << time;
    }
    }
    return 0;

}
