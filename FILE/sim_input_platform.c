#include <linux/module.h>
#include <linux/gpio.h>
#include <linux/io.h>
#include <linux/of.h>
#include <linux/of_gpio.h>
#include <linux/platform_device.h>
#include <linux/input.h>
#include <linux/of_device.h>
#include <linux/interrupt.h>
#include <linux/slab.h>
#include <linux/err.h>

#define UBB_NAME "usb_back_board"

struct ubb_platform_gpio {
	int ubb_int_gpio;
	int ubb_switch_usb;
	int ubb_otg_5v;
};

struct input_dev *ubb_dev;

static struct ubb_platform_gpio *pdata ;

/*
static irqreturn_t ubb_interrupt_thread(int irq, void *data)
{
	printk("%s\n", __func__);

	return IRQ_HANDLED;
}*/

static int ubb_parse_dt(struct platform_device *pdev)
{

	struct device_node *node = pdev->dev.of_node;
	if(node == NULL){
		printk(" device node is NULL\n");
		return 0 ;
	}

	pdata = kzalloc(sizeof(struct ubb_platform_gpio), GFP_KERNEL);
	pdata->ubb_int_gpio = of_get_named_gpio(node, "ubb,gpio-int", 0);
	pdata->ubb_switch_usb = of_get_named_gpio(node, "ubb,gpio-switch-usb", 0);
	pdata->ubb_otg_5v = of_get_named_gpio(node, "ubb,gpio-otg-5v", 0);

	printk("%s: ubb_int_gpio:%d\n", __func__, pdata->ubb_int_gpio);//test

	return 0;
}

static ssize_t ubb_show(struct device *dev,
        struct device_attribute *attr, char *buf)
{
	return sprintf(buf,"This is\n");
}

static ssize_t ubb_store(struct device *dev,
        struct device_attribute *attr, const char *buf,
        size_t count)
{
	char on = *buf;
	if(on == '0'){
		printk("trigger off\n");
	}
	if(on == '1'){
		printk("trigger on\n");
	}
	//input_report_key(ubb_dev, BTN_TRIGGER, 1);
	input_report_key(ubb_dev, BTN_MIDDLE, 1);
	input_report_key(ubb_dev, BTN_MIDDLE, 0);
    //input_report_key(ubb_dev, KEY_CAMERA, 1);
    input_sync(ubb_dev);

	return count;
}

static struct device_attribute ubb_dev_attr = {
    .attr = {
    .name = "ubb_state",
	.mode = S_IRWXU|S_IRWXG|S_IRWXO,
    },
    .show = ubb_show,
    .store = ubb_store,
};

static struct of_device_id ubb_match_table[] = {
	{ .compatible = UBB_NAME,},
	{ },
};
MODULE_DEVICE_TABLE(of, ubb_match_table);

/*
  probe need match_table in dtsi after init
*/
static int ubb_probe(struct platform_device *pdev)
{

	int ret = 0;
	int error = -ENOMEM;

	printk("qiancheng probe %s\n",__func__);

	ubb_dev = input_allocate_device();
	if (!ubb_dev) {
	    printk("qiancheng error input_allocate_device %s\n",__func__);
		return -ENOMEM;
	}

	ubb_dev->name = "ubb";
	ubb_dev->phys = "ubb/input0";
	ubb_dev->id.bustype = BUS_HOST;
	ubb_dev->id.vendor = 0x001f;
	ubb_dev->id.product = 0x0001;
	ubb_dev->id.version = 0x0100;
	ubb_dev->dev.parent = &pdev->dev;

	ubb_dev->evbit[0] = BIT_MASK(EV_KEY) | BIT_MASK(EV_ABS);
	ubb_dev->absbit[0] = BIT_MASK(ABS_X) | BIT_MASK(ABS_Y);
	
	ubb_dev->keybit[BIT_WORD(BTN_MOUSE)] = BIT_MASK(BTN_LEFT) |
			BIT_MASK(BTN_MIDDLE) | BIT_MASK(BTN_RIGHT);
	//ubb_dev->keybit[BIT_WORD(KEY_CAMERA)] = BIT_MASK(KEY_CAMERA) ;



	if (of_match_device(ubb_match_table, &pdev->dev))
		ubb_parse_dt(pdev);

	ret = device_create_file(&(pdev->dev), &ubb_dev_attr);
	if (ret) {
		printk("[ubb_probe] device_create_file failed\n");
	}

    error = input_register_device(ubb_dev);
    if (error) {
        printk("qiancheng input_register_device error:%d\n", error);
        return error;
    }

    platform_set_drvdata(pdev, ubb_dev);

	printk("%s ok\n",__func__);
	return ret;
}

static int ubb_remove(struct platform_device *pdev)
{
	return 0;
}

static int ubb_suspend(struct platform_device *pdev,pm_message_t state)
{
	printk("\nqiancheng %s\n",__func__);
	return 0;
}

static int ubb_resume(struct platform_device *pdev)
{
	printk("\nqiancheng %s\n",__func__);
	return 0;
}

static struct platform_driver ubb_driver = {
	.driver = {
			.name  = UBB_NAME,
			.owner = THIS_MODULE,
			.of_match_table = ubb_match_table,
			},
	.probe   = ubb_probe,
	.remove  = ubb_remove,
	.suspend = ubb_suspend,
	.resume  = ubb_resume,
};

static __init int usb_back_board_init(void)
{
	int ret;
	ret =  platform_driver_register(&ubb_driver);
	printk("\nqiancheng %s\n",__func__);
	if (ret) {
		pr_err("%s(): Failed to register usb_back_board platform driver\n", __func__);
	}
	return ret ;
}

static void __exit usb_back_board_exit(void)
{
	platform_driver_unregister(&ubb_driver);

}

module_init(usb_back_board_init);
module_exit(usb_back_board_exit);
MODULE_AUTHOR("SIMCOM, qiancheng@sim.com");
MODULE_DESCRIPTION("SIMCOM USB back board");
MODULE_LICENSE("GPL");
