/*
 * elevator sstf
 */
#include <linux/blkdev.h>
#include <linux/elevator.h>
#include <linux/bio.h>
#include <linux/module.h>
#include <linux/slab.h>
#include <linux/init.h>

struct sstf_data {
        struct list_head queue;

        sector_t head;
};

void print_list(struct request_queue *q)
{
        struct sstf_data *nd = q->elevator->elevator_data;
        struct list_head *cursor;
        
        printk(KERN_NOTICE "List State: ");
        
        list_for_each(cursor, &nd->queue) {
                struct request *req = list_entry(cursor, struct request, queuelist);
                printk("Item: %llu, ", blk_rq_pos(req));
        }
        printk("\n");
}

static void sstf_merged_requests(struct request_queue *q, struct request *rq,
				 struct request *next)
{
	list_del_init(&next->queuelist);
}

static int sstf_dispatch(struct request_queue *q, int force)
{
	struct sstf_data *nd = q->elevator->elevator_data;

	if (!list_empty(&nd->queue)) {
                struct request *rq;
                printk(KERN_NOTICE "BEFORE DISPATCH\n");
                printk(KERN_NOTICE "HEAD: %llu\n", nd->head);
                print_list(q);

                rq = list_entry(nd->queue.next, struct request, queuelist);
                while (blk_rq_pos(rq) < nd->head) {
                        rq = list_entry(nd->queue.next, struct request, queuelist);
                        nd->head = blk_rq_pos(rq) + blk_rq_sectors(rq);
                }       
                list_del_init(&rq->queuelist);
                nd->head = blk_rq_pos(rq) + blk_rq_sectors(rq);

                printk(KERN_NOTICE "Dispatchint rq: %llu\n", blk_rq_pos(rq));
                elv_dispatch_sort(q, rq);
                printk(KERN_NOTICE "AFTER DISPATCH\n");
                print_list(q);
                printk("\n");
                
                return 1;
        }
	return 0;
}

// Add req to queue
static void sstf_add_request(struct request_queue *q, struct request *rq)
{
        struct sstf_data *nd = q->elevator->elevator_data;
        printk(KERN_NOTICE "BEFORE ADD\n");
        print_list(q);

        printk(KERN_NOTICE "Adding rq: %llu\n", blk_rq_pos(rq));
        // list is empty so just add to tail
        if (list_empty(&nd->queue)) {
                list_add(&rq->queuelist, &nd->queue);
        } else { // list isnt empty so we need to search where to place
        struct request *next, *prev;

        // assign next and prev
        next = list_entry(nd->queue.next, struct request, queuelist);
        prev = next;
        
        /*printk(KERN_NOTICE "iterating request list...");*/
        // compare sector of rq to our next element until we get where we should insert
        while (blk_rq_pos(rq) > blk_rq_pos(next)) {
                /*printk(KERN_NOTICE "list rq: %llu\n", blk_rq_pos(next));*/
                prev = next;
                next = list_entry(next->queuelist.next, struct request, queuelist);
                
                // prev > next so we looped to circular 
                if (blk_rq_pos(prev) > blk_rq_pos(next)) {
                        break;
                }
        }

        /*printk(KERN_NOTICE "Adding request rq: %llu, after prev: %llu\n", */
                        /*blk_rq_pos(rq),*/
                        /*blk_rq_pos(prev));*/

        // Adds after prev and automatically finishes
        list_add(&rq->queuelist, &prev->queuelist);
        printk(KERN_NOTICE "AFTER ADD\n");
        print_list(q);
        printk("\n");
    }
}

// Get former
static struct request *
sstf_former_request(struct request_queue *q, struct request *rq)
{
	struct sstf_data *nd = q->elevator->elevator_data;

	if (rq->queuelist.prev == &nd->queue)
		return NULL;
    // get prev req, one direction so no need?
	return list_entry(rq->queuelist.prev, struct request, queuelist);
}

// Get latter
static struct request *
sstf_latter_request(struct request_queue *q, struct request *rq)
{
	struct sstf_data *nd = q->elevator->elevator_data;

	if (rq->queuelist.next == &nd->queue)
		return NULL;
    // where we need to turn around for the CLook elevator
	return list_entry(rq->queuelist.next, struct request, queuelist);
}

// Create Queue
static int sstf_init_queue(struct request_queue *q, struct elevator_type *e)
{
	struct sstf_data *nd;
	struct elevator_queue *eq;

	eq = elevator_alloc(q, e);
	if (!eq)
		return -ENOMEM;

	nd = kmalloc_node(sizeof(*nd), GFP_KERNEL, q->node);
	if (!nd) {
		kobject_put(&eq->kobj);
		return -ENOMEM;
	}
        nd->head = 0;
	eq->elevator_data = nd;

	INIT_LIST_HEAD(&nd->queue);

	spin_lock_irq(q->queue_lock);
	q->elevator = eq;
	spin_unlock_irq(q->queue_lock);
	return 0;
}

// Quit Queue
static void sstf_exit_queue(struct elevator_queue *e)
{
	struct sstf_data *nd = e->elevator_data;

	BUG_ON(!list_empty(&nd->queue));
	kfree(nd);
}

// Elevator type
static struct elevator_type elevator_sstf = {
	.ops = {
		.elevator_merge_req_fn		= sstf_merged_requests,
		.elevator_dispatch_fn		= sstf_dispatch,
		.elevator_add_req_fn		= sstf_add_request,
		.elevator_former_req_fn		= sstf_former_request,
		.elevator_latter_req_fn		= sstf_latter_request,
		.elevator_init_fn		= sstf_init_queue,
		.elevator_exit_fn		= sstf_exit_queue,
	},
	.elevator_name = "sstf",
	.elevator_owner = THIS_MODULE,
};

// init ??
static int __init sstf_init(void)
{
	return elv_register(&elevator_sstf);
}

// iniit ?
static void __exit sstf_exit(void)
{
	elv_unregister(&elevator_sstf);
}

module_init(sstf_init);
module_exit(sstf_exit);


MODULE_AUTHOR("Michael, Nick, Thai");
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("sstf IO scheduler");
