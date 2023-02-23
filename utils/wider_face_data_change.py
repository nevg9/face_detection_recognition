import argparse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def change_file(local_file, output_file):

    read_bbox_flag = False
    buffer = ""
    out_f = open(output_file, 'w')
    num_bbox = -1
    read_bb = -1
    for line in open(local_file):
        line = line.strip()
        if not read_bbox_flag:
            if line[-3:] == "jpg":
                if read_bb != num_bbox:
                    logger.warning("read bboxs not match,message is:{}".format(buffer.split(" ")[0]))
                else:
                    if buffer != "":
                        out_f.write(buffer + "\n")
                read_bbox_flag = True
                buffer = line
                read_bb = 0
                num_bbox = -1

        else:
            if num_bbox == -1:
                num_bbox = int(line)
            else:
                if num_bbox == 0:
                    read_bbox_flag = False
                read_bb += 1
                bboxs = list(map(int, line.split()[:4]))
                bboxs = [bboxs[0], bboxs[1], bboxs[0] +
                         bboxs[2], bboxs[1]+bboxs[3]]
                buffer += " " + " ".join(map(str, bboxs))
                if read_bb == num_bbox:
                    read_bbox_flag = False

    if buffer != "":
        out_f.write(buffer + "\n")

    out_f.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--wider_face_file', type=str,
                        required=True, help='local path')

    parser.add_argument('-o',
                        '--output_file',
                        type=str,
                        required=True, help='chang file local path')

    args = parser.parse_args()
    change_file(args.wider_face_file, args.output_file)