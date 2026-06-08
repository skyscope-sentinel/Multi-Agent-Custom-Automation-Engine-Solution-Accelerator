mod integrations;
mod autonomy;

use iced::widget::{column, container, text, button, scrollable, row};
use iced::{Alignment, Element, Length, Sandbox, Settings, Theme};

pub fn main() -> iced::Result {
    SkyscopeSentinel::run(Settings::default())
}

struct SkyscopeSentinel {
    developer: String,
    business_name: String,
    status: String,
    logs: Vec<String>,
}

#[derive(Debug, Clone)]
enum Message {
    ActivateScaling,
    LogUpdate(String),
}

impl Sandbox for SkyscopeSentinel {
    type Message = Message;

    fn new() -> Self {
        Self {
            developer: String::from("Casey Jay Topojani"),
            business_name: String::from("Skyscope Sentinel Intelligence"),
            status: String::from("Idle"),
            logs: vec![String::from("System initialized.")],
        }
    }

    fn title(&self) -> String {
        format!("{} - Autonomous Command Center", self.business_name)
    }

    fn update(&mut self, message: Message) {
        match message {
            Message::ActivateScaling => {
                self.status = String::from("Scaling Protocols Active");
                self.logs.push(String::from("Scaling directive activated: All systems maximizing output."));
                self.logs.push(String::from("Developer: Casey Jay Topojani."));
            }
            Message::LogUpdate(log) => {
                self.logs.push(log);
            }
        }
    }

    fn view(&self) -> Element<Message> {
        let title = text(&self.business_name).size(40);
        let dev_info = text(format!("Lead Developer: {}", self.developer)).size(18);
        let status_display = text(format!("System Status: {}", self.status)).size(24);

        let activate_button = button("Initiate Global Scaling")
            .padding(10)
            .on_press(Message::ActivateScaling);

        let logs_column = column(
            self.logs.iter().map(|log| text(log).size(14).into()).collect()
        ).spacing(5);

        let logs_scroll = scrollable(logs_column)
            .height(Length::Fixed(300.0))
            .width(Length::Fill);

        let content = column![
            title,
            dev_info,
            status_display,
            activate_button,
            text("System Logs:").size(20),
            logs_scroll,
        ]
        .spacing(20)
        .align_items(Alignment::Center);

        container(content)
            .width(Length::Fill)
            .height(Length::Fill)
            .padding(20)
            .center_x()
            .center_y()
            .into()
    }

    fn theme(&self) -> Theme {
        Theme::Dark
    }
}
