import numpy as np
import cv2
import csv

def basic(source,target,num,dis,name,distance):
    (SB, SG, SR) = cv2.split(source)
    (TB, TG, TR) = cv2.split(target)
    #weight(SR,np.mean(SR),np.std(SR),np.mean(TR),np.std(TR),'red')
    temp=[np.mean(SR),np.std(SR),np.mean(TR),np.std(TR),  #0 1 2 3
          np.mean(SG),np.std(SG),np.mean(TG),np.std(TG),  #4 5 6 7
          np.mean(SB),np.std(SB),np.mean(TB),np.std(TB),] #8 9 10 11
    weight=[100,100,100,100,100,100]
    w=0.00
    with open('../distance-'+dis+'/res-0'+str(num)+'-dist-blue.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([name])
        writer.writerow(["NO"]+["Weight"]+["D(S, Iw)"]+["D(T, Iw)"]+["Difference"])
        with open('../distance-'+dis+'/res-0'+str(num)+'-dist-green.csv', 'w', newline='') as csvfile:
            writer1 = csv.writer(csvfile)
            writer1.writerow([name])
            writer1.writerow(["NO"]+["Weight"]+["D(S, Iw)"]+["D(T, Iw)"]+["Difference"])
            with open('../distance-'+dis+'/res-0'+str(num)+'-dist-red.csv', 'w', newline='') as csvfile:
                writer2 = csv.writer(csvfile)
                writer2.writerow([name])
                writer2.writerow(["NO"]+["Weight"]+["D(S, Iw)"]+["D(T, Iw)"]+["Difference"])
                for i in range(101):
                    R=(((w*temp[3]+(1-w)*temp[1])/temp[1])*(SR-temp[0])+w*temp[2]+(1-w)*temp[0])
                    G=(((w*temp[7]+(1-w)*temp[5])/temp[5])*(SG-temp[4])+w*temp[6]+(1-w)*temp[4])
                    B=(((w*temp[11]+(1-w)*temp[9])/temp[9])*(SB-temp[8])+w*temp[10]+(1-w)*temp[8])
                    weight_img = cv2.merge([B, G, R])
                    weight_img = np.clip(weight_img,0,255).astype(np.uint8)
                    hist=calc_hist_distances(source, target, weight_img, distance)
                    writer.writerow([num]+[w]+[round(hist[0][0],6)]+[round(hist[0][1],6)]+[round(hist[0][2],6)])
                    writer1.writerow([num]+[w]+[round(hist[1][0],6)]+[round(hist[1][1],6)]+[round(hist[1][2],6)])
                    writer2.writerow([num]+[w]+[round(hist[2][0],6)]+[round(hist[2][1],6)]+[round(hist[2][2],6)])
                    if(hist[0][2]<weight[0]):
                        weight[1]=w
                        weight[0]=hist[0][2]
                    if(hist[1][2]<weight[2]):
                        weight[3]=w
                        weight[2]=hist[1][2]
                    if(hist[2][2]<weight[4]):
                        weight[5]=w
                        weight[4]=hist[2][2]
                    w+=0.01
                    
    R=(((weight[5]*temp[3]+(1-weight[5])*temp[1])/temp[1])*(SR-temp[0])+weight[5]*temp[2]+(1-weight[5])*temp[0])
    G=(((weight[3]*temp[7]+(1-weight[3])*temp[5])/temp[5])*(SG-temp[4])+weight[3]*temp[6]+(1-weight[3])*temp[4])
    B=(((weight[1]*temp[11]+(1-weight[1])*temp[9])/temp[9])*(SB-temp[8])+weight[1]*temp[10]+(1-weight[1])*temp[8])
    weight_img = cv2.merge([B, G, R])
    weight_img = np.clip(weight_img,0,255).astype(np.uint8)
    cv2.imwrite('../awctresult-'+dis+'/' + 'res-0'+str(num)+'-'+str(round(weight[1],3))+'-'+str(round(weight[3],3))+'-'+str(round(weight[5],3))+'.png',weight_img)
    
def calc_hist_distances(source, target, weighted_transfer, distance):
    # Compute the histograms for each channel of the source, target and weighted transfer images
    num_bins = 256
    bin_range = (0, 256)
    source_hist = [cv2.calcHist([source], [c], None, [num_bins], bin_range) for c in range(3)]
    target_hist = [cv2.calcHist([target], [c], None, [num_bins], bin_range) for c in range(3)]
    weighted_transfer_hist = [cv2.calcHist([weighted_transfer], [c], None, [num_bins], bin_range) for c in range(3)]

    # Normalize the histograms
    for c in range(3):
        source_hist[c] /= source.size
        target_hist[c] /= target.size
        weighted_transfer_hist[c] /= weighted_transfer.size

    # Compute the distances between the histograms for each channel
    hist_distance = []
    for channel in range(3):
        hist_distance_source = cv2.compareHist(source_hist[channel], weighted_transfer_hist[channel], distance)
        hist_distance_target = cv2.compareHist(target_hist[channel], weighted_transfer_hist[channel], distance)
        diff_hist_distance = abs(hist_distance_source - hist_distance_target)
        hist_distance.append([hist_distance_source, hist_distance_target, diff_hist_distance])
    return hist_distance

def wct(dis,name,distance):
    for i in range(1,7):
        s_img = cv2.imread('../awctresult-'+dis+'/' + 'sou-0'+str(i)+'.png')
        t_img = cv2.imread('../awctresult-'+dis+'/' + 'tar-0'+str(i)+'.png')
        basic(s_img, t_img,i,dis,name,distance)

        
wct("COR","Correlation Distance",cv2.HISTCMP_CORREL)
wct("CNS","Chi-Square Distance",cv2.HISTCMP_CHISQR)
wct("INS","Intersection Distance",cv2.HISTCMP_INTERSECT)
wct("BHA","Bhattacharyya Distance",cv2.HISTCMP_BHATTACHARYYA)