#include <linux/module.h>
#include <linux/gpio.h>
#include <linux/io.h>
#include <linux/of.h>
#include <linux/of_gpio.h>
#include <linux/platform_device.h>
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

static struct ubb_platform_gpio *pdata ;

static irqreturn_t ubb_interrupt_thread(int irq, void *data)
{
	printk("%s\n", __func__);

	if (gpio_get_value(pdata->ubb_int_gpio)) { //no connect
		gpio_set_value(pdata->ubb_switch_usb, 0);
		gpio_set_value(pdata->ubb_otg_5v, 0);
		gpio_set_value(110, 1);
		pr_err("+++%s, interr:%d\n", __func__, gpio_get_value(pdata->ubb_int_gpio));
	}
	else { //connecting
		gpio_set_value(pdata->ubb_switch_usb, 1);
		gpio_set_value(pdata->ubb_otg_5v, 1);
		gpio_set_value(110, 0);
		pr_err("---%s, interr:%d\n", __func__, gpio_get_value(pdata->ubb_int_gpio));
	}

	return IRQ_HANDLED;
}

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
		gpio_set_value(pdata->ubb_int_gpio, 0);
	}
	if(on == '1'){
		printk("trigger on\n");
		gpio_set_value(pdata->ubb_int_gpio, 1);
	}

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
	int irq;

	printk("probe %s\n",__func__);

	if (of_match_device(ubb_match_table, &pdev->dev))
		ubb_parse_dt(pdev);

	ret = device_create_file(&(pdev->dev), &ubb_dev_attr);
	if (ret) {
		printk("[ubb_probe] sys file creation failed\n");
	}

	if (gpio_is_valid(pdata->ubb_int_gpio)) {
		gpio_request(pdata->ubb_switch_usb, "ubb_switch_usb");
		gpio_request(pdata->ubb_otg_5v, "ubb_otg_5v");
		ret = gpio_request(pdata->ubb_int_gpio, "usb_back_board_int");
		if (ret) {
			printk("%s: unable to request interrupt gpio %d\n", __func__,
				pdata->ubb_int_gpio);
		}
	}

	ret = gpio_direction_input(pdata->ubb_int_gpio);
	if (ret) {
		printk("%s: unable to set direction for gpio %d\n", __func__, pdata->ubb_int_gpio);
	}

	irq = gpio_to_irq(pdata->ubb_int_gpio);

	ret = request_threaded_irq(irq, NULL, ubb_interrupt_thread,
				     IRQF_TRIGGER_RISING | IRQF_TRIGGER_FALLING | IRQF_ONESHOT,
				     "usb_back_board", NULL);
	if (ret) {
		printk("[ubb_probe] can't get IRQ %d, error %d\n", irq, ret);
	}

	ret = gpio_direction_output(pdata->ubb_switch_usb, 0);
	if (ret) {
		printk("%s: unable to set direction for gpio %d\n", __func__, pdata->ubb_switch_usb);
	}
	
	ret = gpio_direction_output(pdata->ubb_otg_5v, 0);
	if (ret) {
		printk("%s: unable to set direction for gpio %d\n", __func__, pdata->ubb_otg_5v);
	}

	//enable_irq(irq);
	//disable_irq(irq);

	printk("%s ok\n",__func__);
	return ret;
}

static int ubb_remove(struct platform_device *pdev)
{
	return 0;
}

static int ubb_suspend(struct platform_device *pdev,pm_message_t state)
{
	return 0;
}

static int ubb_resume(struct platform_device *pdev)
{
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
	printk("\n %s\n",__func__);
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
