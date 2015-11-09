#include <stdio.h>
#include <stdlib.h>
#include <algorithm>

//0-12 spades, 0 suite
//13-25 hearts, 1 suite
//26-38 diamonds, 2
//39-51 clubs, 3

int suite(int card) {
  return card / 13;
}

int face(int card) {
  return card % 13;
}

void printc(int card)
{
  int s = suite(card);
  int f = face(card);

  if(s == 0)
    {
      printf("spade ");
    }
  else if(s == 1)
    {
      printf("heart ");
    }
  else if(s == 2)
    {
      printf("diamond ");
    }
  else
    {
      printf("club ");
    }

  printf("%d\n", f);
}

float value(int *hand, int *table)
{
  int *tface = (int *)malloc(7 * sizeof(int));
  int *tsuite = (int *)malloc(7 * sizeof(int));

  for(int i = 0; i < 2; i++)
    {
      tface[i] = face(hand[i]);
      tsuite[i] = suite(hand[i]);
    }

  for(int i = 2; i < 7; i++)
    {
      tface[i] = face(table[i - 2]);
      tsuite[i] = suite(table[i - 2]);
    }

  std::sort(tface, tface + 7);
  std::sort(tsuite, tsuite + 7);

  int high = tface[6]; // high card

  //pair(hand, table); // -1 not pair, 8 pair of eights
  int pair = -1;
  for(int i = 6; i > 1; i--)
    {
      if(tface[i] == tface[i - 1])
        {
          pair = i;
          break;
        }
    }

  //twopair(hand, table); // -1 not 2 pair, returns sum of pairs
  int twopair = -1;
  if(pair > -1)
    {
      for(int i = pair - 2; i > 1; i--)
        {
          if(tface[i] == tface[i - 1])
            {
              twopair = i;
              break;
            }
        }
    }

  //threeofakind(hand, table); // -1, value of card
  int threeofakind = -1;
  if(pair > -1)
    {
      for(int i = pair; i > 2; i--)
        {
          if(tface[i] == tface[i - 1] && tface[i - 1] == tface[i - 2])
            {
              threeofakind = i;
              break;
            }
        }
    }

  //straight(hand, table); // -1, largest card
  int straight = -1;
  int straightsuite = -1;

  int s = 0;

  int *tface2 = (int *)malloc(8 * sizeof(int));
  int *tsuite2 = (int *)malloc(8 * sizeof(int));

  tface2[0] = tface[0];
  for(int i = 1; i < 7; i++)
    {
      if(tface[i] != tface[i - 1])
        {
          tface2[s] = tface[i];
          tsuite2[s] = tsuite[i];
          s++;
        }
    }

  if(s >= 5)
    {
      for(int i = s - 1; i > 3; i--)
        {
          if(tface2[i] - 1 == tface2[i - 1] &&
             tface2[i] - 2 == tface2[i - 2] &&
             tface2[i] - 3 == tface2[i - 3] &&
             tface2[i] - 4 == tface2[i - 4])
            {
              straight = tface2[i];
              straightsuite = tsuite2[i];
            }
        }

      if(straight == -1 && tface[6] == 12)
        {
          if(tface2[3] == 3 &&
             tface2[2] == 2 &&
             tface2[1] == 1 &&
             tface2[0] == 0)
            {
              straight = 3;
              straightsuite = tsuite2[3];
            }
        }
    }

  free(tface2);
  free(tsuite2);

  //flush(hand, table); // -1, highest card
  int flush = -1;
  int flushsuite = -1;
  int *cs = (int *)malloc(4 * sizeof(int));
  int *ms = (int *)malloc(4 * sizeof(int));
  cs[0] = 0;
  cs[1] = 0;
  cs[2] = 0;
  cs[3] = 0;

  ms[0] = 0;
  ms[1] = 0;
  ms[2] = 0;
  ms[3] = 0;

  for(int i = 0; i < 6; i++)
    {
      cs[tsuite[i]] += 1;
      ms[tsuite[i]] = std::max(ms[tsuite[i]], tface[i]);
    }

  if(cs[0] >= 5)
    {
      flush = ms[0];
      flushsuite = 0;
    }

  if(cs[1] >= 5)
    {
      flush = ms[1];
      flushsuite = 1;
    }

  if(cs[2] >= 5)
    {
      flush = ms[2];
      flushsuite = 2;
    }

  if(cs[3] >= 5)
    {
      flush = ms[3];
      flushsuite = 3;
    }

  free(cs);
  free(ms);

  //fullhouse(hand, table); // -1, highest triple
  int fullhouse = -1;
  if(threeofakind > -1 && twopair > -1)
    fullhouse = tface[threeofakind];

  //fourofakind(hand, table); // -1, card value
  int fourofakind = -1;
  if(threeofakind > -1)
    for(int i = threeofakind; i > 3; i--)
      {
        if(tface[i] == tface[i - 1] &&
           tface[i] == tface[i - 2] &&
           tface[i] == tface[i - 3])
          {
            fourofakind = i;
          }
      }

  //straightflush(hand, table); // -1, highest card
  int straightflush = -1;
  if(straight > -1 && flush > -1 && flushsuite == straightsuite)
    straightflush = straight;

  //high
  pair = tface[pair];
  twopair = tface[twopair];
  threeofakind = tface[threeofakind];
  //straight
  //flush
  //fullhouse
  fourofakind = tface[fourofakind];
  //straightflush

  free(tface);
  free(tsuite);

  if(straightflush > -1)
    return 13 * 8 + straightflush;

  if(fourofakind > -1)
    return 13 * 7 + fourofakind;

  if(fullhouse > -1)
    return 13 * 6 + fullhouse;

  if(flush > -1)
    return 13 * 5 + flush;

  if(straight > -1)
    return 13 * 4 + straight;

  if(threeofakind > -1)
    return 13 * 3 + threeofakind;

  if(twopair > -1)
    return 13 * 2 + twopair;

  if(pair > -1)
    return 13 * 1 + pair;

  return tface[6];
}

int win(int *hand0, int *hand1, int *table)
{
  float value0 = value(hand0, table);
  float value1 = value(hand1, table);

  if(value0 == value1)
    {
      if(face(hand0[0]) == face(hand0[1]) && face(hand1[0]) == face(hand1[1]))
        {
          return face(hand0[0]) > face(hand1[0]);
        }
      else if(face(hand0[0]) == face(hand0[1]))
        {
          return true;
        }
      else if(face(hand1[0]) == face(hand1[1]))
        {
          return false;
        }
      else
        {
          return std::max(face(hand0[0]), face(hand0[1])) > std::max(face(hand0[0]), face(hand0[1]));
        }
    }
  else
    {
      return value0 > value1;
    }
}

int main(int argc, char **argv) {
  long int total = 0;

  int *hand0 = (int *)malloc(2 * sizeof(int));
  int *hand1 = (int *)malloc(2 * sizeof(int));
  int *table = (int *)malloc(5 * sizeof(int));

  hand0[0] = rand() % 52;
  hand0[1] = rand() % 52;

  printf("We have:\n");
  printc(hand0[0]);
  printc(hand0[1]);

  int nhands = 0;
  int nwins = 0;

  //for(int i = 0; i < 50; i++)
  //for(int j = i + 1; j < 50; j++)
      {
        int i = 5;
        int j = 43;
        printf("%d %d\n", i, j);
        hand1[0] = i;
        hand1[1] = j;
        printf("He has:\n");
        printc(hand1[0]);
        printc(hand1[1]);
        for(int k = j + 1; k < 50; k++)
          for(int l = k + 1; l < 50; l++)
            for(int m = l + 1; m < 50; m++)
              for(int n = m + 1; n < 50; n++)
                for(int o = n + 1; o < 50; o++)
                  {
                    table[0] = k;
                    table[1] = l;
                    table[2] = m;
                    table[3] = n;
                    table[4] = o;

                    if(win(hand0, hand1, table))
                      nwins += 1;
                    
                    nhands += 1;
                  }
      }
  
  printf("percent win (max 1.0) %f\n", float(nwins) / float(nhands));

  free(hand0);
  free(hand1);
  free(table);

  printf("%ld\n", total);
}

